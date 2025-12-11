import os
from dotenv import load_dotenv
from pathlib import Path
import langchain.messages
from langchain_openai import ChatOpenAI

import shutil


from tools import create_calendar_event, get_persons, get_calendars

load_dotenv(override=True)

current_file = Path(__file__)
output_dir = f"{current_file.parent.parent}/schedule/updated_calendars"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.mkdir(output_dir)

# Client & Model
llm = ChatOpenAI(
    model="gpt-5.1",
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=lambda: os.environ["OPENAI_API_KEY"],
)
tools = {
    "create_calendar_event": create_calendar_event,
    "get_persons": get_persons,
    "get_calendars": get_calendars,
}
llm_with_tools = llm.bind_tools(tools.values())
prompt = (
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
messages = [
    langchain.messages.SystemMessage(prompt),
    langchain.messages.HumanMessage(
        "Book some meetings for Daniel Åsberg for 2025-12-01."
    ),
]

# Get tool calls
response = None
while response is None or response.tool_calls:
    response = llm_with_tools.invoke(messages)
    messages.append(response)
    for tool_call in response.tool_calls:
        selected_tool = tools[tool_call["name"]]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)

# Display output
for msg in messages:
    func_call = msg.additional_kwargs.get("tool_calls", [{}])[-1].get("function", {})
    if func_call:
        ...
        # tool_content = f"{func_call.get('name')}({func_call.get('arguments')})".replace(
        #     ":", ": "
        # ).replace(",", ", ")
        # print(f"tool_call: {tool_content}")
    else:
        print(f"{msg.type}: {msg.content}")
