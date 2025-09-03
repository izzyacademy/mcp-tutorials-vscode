from typing import Any

from mcp import ClientSession
from mcp.shared.context import RequestContext
from mcp.types import ElicitRequestParams, ElicitResult
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.messages import ModelRequest, ModelResponse
from pydantic_ai.models.openai import OpenAIChatModel, OpenAIModelName
from rich.prompt import Prompt

model_name: OpenAIModelName = 'gpt-4o-mini'

ai_foundry_model = OpenAIChatModel(model_name=model_name, provider='azure')

instructions = """
You are an AI agent named Eagle. 

You help passengers to search for flights, retrieve details about passenger travel documents like passports.

You can also check what dates flights are available from the service.
"""

async def handle_elicitation(
    context: RequestContext[ClientSession, Any, Any],
    params: ElicitRequestParams,
) -> ElicitResult:
    """Handle elicitation requests from MCP server."""
    print(f'\n{params.message}')

    if not params.requestedSchema:
        response = Prompt.ask('Response: ')
        return ElicitResult(action='accept', content={'response': response})

    # Collect data for each field
    properties = params.requestedSchema['properties']
    data = {}

    for field, info in properties.items():
        description = info.get('description', field)

        value = Prompt.ask(f'{description}: ')

        # Convert to proper type based on JSON schema
        if info.get('type') == 'integer':
            data[field] = int(value)
        else:
            data[field] = value

    # Confirm
    confirm = Prompt.ask('\nConfirm booking? (y/n/c): ').lower()

    if confirm == 'y':
        print('Booking details:', data)
        return ElicitResult(action='accept', content=data)
    elif confirm == 'n':
        return ElicitResult(action='decline')
    else:
        return ElicitResult(action='cancel')

async def thank_you_message():
    print("\n\nThank you for using the Flight Search Agent. Have a wonderful day\n\n")


async def main():
    flight_service_definition = MCPServerStreamableHTTP(url='http://localhost:8000/mcp', elicitation_callback=handle_elicitation)
    mcp_servers: list[MCPServerStreamableHTTP] = [flight_service_definition]

    # Keeping track of the Message history
    message_history: list[ModelRequest | ModelResponse] = []

    # initial prompt to get started
    current_prompt = "\nHow can I help you?"

    while True:

        user_prompt = Prompt.ask(current_prompt)
        employee_experience_agent = Agent(ai_foundry_model, instructions=instructions, toolsets=mcp_servers)
        results = await employee_experience_agent.run(user_prompt, message_history=message_history)
        print(results.output)
        message_history = results.all_messages()

        exit_or_not = Prompt.ask("\nIs there anything else you would like me to assist you with?", choices=['y', 'n'])

        if exit_or_not == 'n':
            await thank_you_message()
            break
        current_prompt = "\nWhat else would you like me to help you with?"


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
