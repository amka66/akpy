"""
This module (the entry point to this package) defines the main function for the package
"""

import asyncio
import sys

import typer
from pydantic import SecretStr
from rich import print

from .config import GeneralInfo, MyBaseSecrets, MyBaseSettings
from .utils import create_logger


class EntrySettings(MyBaseSettings):
    """This class contains module-level settings"""

    sleep_time: float = 3.0


class _EntrySecrets(MyBaseSecrets):
    """This class contains module-level secrets"""

    secret_message: SecretStr = SecretStr(
        "Set your secret message at file '.secret' at the specified location. This is a stub."
    )


# Get info, settings, and secrets
_info = GeneralInfo()
_settings = EntrySettings()
_secrets = _EntrySecrets()

# Initialize the app
_app = typer.Typer()

# Create the logger
_logger = create_logger(__name__)
_log_message_prefix = f"system {sys.version} - package {_info.version}"


async def _async_example(sleep_time: float) -> None:
    """
    An example for an async function that sleeps for a given amount of time
    """

    print()
    print(rf'"{_secrets.secret_message.get_secret_value()}"')
    print()
    print("Think about it...")
    _logger.info(
        "%s - sleeping for %s seconds - started", _log_message_prefix, sleep_time
    )
    await asyncio.sleep(sleep_time)
    _logger.info(
        "%s - sleeping for %s seconds - ended", _log_message_prefix, sleep_time
    )


@_app.command()
def go(sleep_time: float = _settings.sleep_time) -> None:
    """This is the main and only command"""
    asyncio.run(_async_example(sleep_time))


def main() -> None:
    """Run the app"""
    _app(prog_name=_info.project_name)
