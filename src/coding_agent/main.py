import os

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider


def _getenv(key: str) -> str:
    result = os.getenv(key)
    if result is None:
        raise ValueError(f"Environment variable `{key}` not set")
    return result


_OPENAI_API_BASE = _getenv("OPENAI_API_BASE")
_OPENAI_API_KEY = _getenv("OPENAI_API_KEY")
_MODEL = _getenv("MODEL")

_AGENT_NAME = "coding-agent"


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
    )

    agent.to_cli_sync(prog_name=_AGENT_NAME)
