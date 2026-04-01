import os

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from coding_agent.tools import (
    delete_file,
    read_file,
    search_files,
    write_file,
)


def _getenv(key: str) -> str:
    result = os.getenv(key)
    if result is None:
        raise ValueError(f"Environment variable `{key}` not set")
    return result


_OPENAI_API_BASE = _getenv("OPENAI_API_BASE")
_OPENAI_API_KEY = _getenv("OPENAI_API_KEY")
_MODEL = _getenv("MODEL")

_AGENT_NAME = "coding-agent"

_INSTRUCTIONS = (
    "You are Python coding agent.\n"
    "* Write clear, correct, and minimal Python code.\n"
    "* Follow the user's instructions exactly, do not add extra features.\n"
    "* Prefer standard library over external dependencies unless explicitly specified.\n"
    "* If requirements are unclear, ask a concise clarification question.\n"
    "* Provide a brief summary of your implementation.\n"
    "* Use the available tools.\n"
    "* Use relative file paths."
)


def main() -> None:
    provider = OpenAIProvider(
        base_url=_OPENAI_API_BASE,
        api_key=_OPENAI_API_KEY,
    )

    model = OpenAIChatModel(
        model_name=_MODEL,
        provider=provider,
    )

    agent = Agent(
        model=model,
        instructions=_INSTRUCTIONS,
        tools=[read_file, write_file, search_files, delete_file],
    )

    agent.to_cli_sync(prog_name=_AGENT_NAME)
