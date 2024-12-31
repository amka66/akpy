"""
This module (the entry point to this package) defines the main function for the package
"""

import asyncio
import sys

import typer
from openai import AsyncAzureOpenAI
from pydantic import SecretStr
from rich import print

from .config import GeneralInfo, GeneralSettings, MyBaseSecrets
from .llmapi import CACHE_FILENAME, TokenManager, client_kwargs, model_kwargs
from .utils import create_logger


class EntrySettings(GeneralSettings):
    """This class contains module-level settings"""

    system_prompt: str


class _EntrySecrets(MyBaseSecrets):
    """This class contains module-level secrets for accessing the API"""

    model_chat_completion: SecretStr
    model_embedding: SecretStr


# Get general info
_info = GeneralInfo()

# Get module's settings and secrets
_settings = EntrySettings()
_secrets = _EntrySecrets()

# Initialize the app
_app = typer.Typer()

# Create the logger
_logger = create_logger(__name__)


async def _generate_output_and_embed(system_prompt: str) -> None:
    """
    Generate output according to the provided system prompt
    and generate an embedding of the output
    """

    # Initialize the client
    client = AsyncAzureOpenAI(
        **client_kwargs(
            token_provider=TokenManager(
                cache_file=_info.cache_dir / CACHE_FILENAME
            ).get_token,
        )
    )

    # Set system message
    print()
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
    ]
    print("# Messages:")
    print(messages)

    # Generate content for the given a prompt and print it
    print()
    response1 = await client.chat.completions.create(
        **model_kwargs(
            _secrets.model_chat_completion.get_secret_value(),
        ),
        messages=messages,
        max_tokens=100,
        temperature=0.7,
    )
    _logger.info(
        "system %s - package %s - model %s",
        sys.version,
        _info.version,
        response1.model,
    )
    output = response1.choices[0].message.content
    if not output:
        raise RuntimeError("Failed to generate output")
    print("# Generated:")
    print(output)

    # Generate an embedding of the output and print it
    print()
    response2 = await client.embeddings.create(
        **model_kwargs(
            _secrets.model_embedding.get_secret_value(),
        ),
        input=output,
        encoding_format="float",
    )
    _logger.info(
        "system %s - package %s - model %s",
        sys.version,
        _info.version,
        response2.model,
    )
    embedding = response2.data[0].embedding
    if not embedding:
        raise RuntimeError("Failed to generate embedding")
    print("# Embedding:")
    print(str(embedding[:10])[:-1] + "...")


@_app.command()
def go(system_prompt: str = _settings.system_prompt) -> None:
    """This is the main and only command"""
    asyncio.run(_generate_output_and_embed(system_prompt))


def main() -> None:
    """Run the app"""
    _app(prog_name=_info.project_name)
