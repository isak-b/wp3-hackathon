import logging
import os
import sys

import click
import httpx
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import (BasePushNotificationSender,
                              InMemoryPushNotificationConfigStore, InMemoryTaskStore)
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from dotenv import load_dotenv

from .agent import EmployeeCatalogAgent
from .agent_executor import EmployeeCatalogAgentExecutor

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingURLError(Exception):
    """Exception for missing URL."""


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""


@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=8011)
def main(host, port):
    """Starts the Employee Catalog Agent server."""
    try:
        if not os.getenv('OPENAI_BASE_URL'):
            raise MissingURLError(
                'OPENAI_BASE_URL environment variable not set.'
            )
        if not os.getenv('OPENAI_API_KEY'):
            raise MissingAPIKeyError(
                'OPENAI_API_KEY environment variable not set.'
            )

        capabilities = AgentCapabilities(streaming=True, push_notifications=True)
        skills = [
            AgentSkill(
                id='get_employee_info',
                name='Get Employee Information Tool',
                description='Helps with retrieving information about current employees',
                tags=['employee information'],
                examples=[
                    'What is the name of the employee with id 3?',
                    'How many employees do we have?',
                    'What is the id of Jane Doe?'
                ],
            ),
        ]
        agent_card = AgentCard(
            name='Employee Catalog Agent',
            description=(
                'Helps with queries and updates to the employee catalog service'),
            url=f'http://{host}:{port}/',
            version='1.0.0',
            default_input_modes=EmployeeCatalogAgent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=EmployeeCatalogAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=skills,
        )

        # --8<-- [start:DefaultRequestHandler]
        httpx_client = httpx.AsyncClient()
        push_config_store = InMemoryPushNotificationConfigStore()
        push_sender = BasePushNotificationSender(httpx_client=httpx_client,
                                                 config_store=push_config_store)
        request_handler = DefaultRequestHandler(
            agent_executor=EmployeeCatalogAgentExecutor(),
            task_store=InMemoryTaskStore(),
            push_config_store=push_config_store,
            push_sender=push_sender
        )
        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

        uvicorn.run(server.build(), host=host, port=port)
        # --8<-- [end:DefaultRequestHandler]

    except MissingAPIKeyError as e:
        logger.error(f'Error: {e}')
        sys.exit(1)
    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
