import os
import shutil
import pydantic
import typing
from dotenv import load_dotenv
from pathlib import Path

import langchain.messages
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from tools import create_calendar_event, get_persons, get_calendars

load_dotenv(override=True)
current_file = Path(__file__)

memory = MemorySaver()


class ResponseFormat(pydantic.BaseModel):
    """Respond to the user in this format."""

    status: typing.Literal['input_required', 'completed', 'error'] = 'input_required'
    message: str


class Scheduler:
    def __init__(self):
        output_dir = f"{current_file.parent.parent}/schedule/updated_calendars"
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.mkdir(output_dir)

        self.SYSTEM_INSTRUCTION = (
            "You are a professional scheduler.\n"
            "Your task is to plan and schedule meetings for a new employee with their manager and colleague.\n"
            "Guidelines:\n"
            "- Book 1-on-1 meetings with relevant persons\n"
            "- Book at least one meet-and-greet\n"
            "- You must not book at times when the persons already have meetings.\n"
            "- Set suitable meeting durations (e.g. 30 or 60 minutes)\n"
            "- Assume that everyone works 8 - 17 with lunch at 12\n"
            "- Update the calendars for all meeting participants.\n"
        )
        self.FORMAT_INSTRUCTION = (
            'Set response status to input_required if the user needs to provide more information to complete the request.'
            'Set response status to error if there is an error while processing the request.'
            'Set response status to completed if the request is complete.'
        )
        self.SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

        # Client & Model
        self.llm = ChatOpenAI(
            model="gpt-5.1",
            base_url=os.environ["OPENAI_BASE_URL"],
            api_key=lambda: os.environ["OPENAI_API_KEY"],
        )

        # Tools
        self.tools = [create_calendar_event, get_persons, get_calendars]
        self.graph = create_react_agent(
            self.llm,
            tools=self.tools,
            checkpointer=memory,
            prompt=self.SYSTEM_INSTRUCTION,
            response_format=(self.FORMAT_INSTRUCTION, ResponseFormat),
        )

    async def stream(self, query, context_id) -> typing.AsyncIterable[dict[str, any]]:
        inputs = {'messages': [('user', query)]}
        config = {'configurable': {'thread_id': context_id}}

        for item in self.graph.stream(inputs, config, stream_mode='values'):
            message = item['messages'][-1]
            if (
                isinstance(message, langchain.messages.AIMessage)
                and message.tool_calls
                and len(message.tool_calls) > 0
            ):
                yield {
                    'is_task_complete': False,
                    'require_user_input': False,
                    'content': 'Calling tools...'
                }
            elif isinstance(message, langchain.messages.ToolMessage):
                yield {
                    'is_task_complete': False,
                    'require_user_input': False,
                    'content': 'Processing message...',
                }

        yield self.get_agent_response(config)

    def get_agent_response(self, config):
        current_state = self.graph.get_state(config)
        structured_response = current_state.values.get('structured_response')
        if structured_response and isinstance(
            structured_response, ResponseFormat
        ):
            if structured_response.status == 'input_required':
                return {
                    'is_task_complete': False,
                    'require_user_input': True,
                    'content': structured_response.message,
                }
            if structured_response.status == 'error':
                return {
                    'is_task_complete': False,
                    'require_user_input': True,
                    'content': structured_response.message,
                }
            if structured_response.status == 'completed':
                return {
                    'is_task_complete': True,
                    'require_user_input': False,
                    'content': structured_response.message,
                }

        return {
            'is_task_complete': False,
            'require_user_input': True,
            'content': (
                'We are unable to process your request at the moment. '
                'Please try again.'
            ),
        }
