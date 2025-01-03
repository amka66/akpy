"""
This module (the entry point to this package) defines the main function for the package
"""

import asyncio

import typer
from pydantic import SecretStr
from rich import print

from .config import (
    MyBaseSecrets,
    MyBaseSettings,
    config_dir,
    create_logger_module,
    package_name,
)


class EntrySettings(MyBaseSettings):
    """This class contains module-level settings"""

    sleep_time: float = 3.0


class _EntrySecrets(MyBaseSecrets):
    """This class contains module-level secrets"""

    secret_message: SecretStr = SecretStr(
        f"Set your secret message in file '{config_dir / '.secret'}'. This is a stub."
    )


# Get info, settings, and secrets
_settings = EntrySettings()
_secrets = _EntrySecrets()

# Initialize the app
_app = typer.Typer()

# Create the logger
_logger = create_logger_module(__name__)


async def _async_example(sleep_time: float) -> None:
    """
    An example for an async function that sleeps for a given amount of time
    """

    print()
    print(f"{_secrets.secret_message.get_secret_value()}")
    print("Think about it...")
    _logger.info("sleeping for %s seconds - started", sleep_time)
    await asyncio.sleep(sleep_time)
    _logger.info("sleeping for %s seconds - ended", sleep_time)


@_app.command()
def go(sleep_time: float = _settings.sleep_time) -> None:
    """This is the main and only command"""
    asyncio.run(_async_example(sleep_time))


def main() -> None:
    """Run the app"""
    _app(prog_name=package_name)
