"""
This module includes base definitions toward module-level concrete definitions.
This includes abstract base classes for storing settings and secrets, as well as logger creation.
The module also possibly includes concrete package-level classes for settings and secrets.
"""

import logging
import sys
from abc import ABC
from importlib.metadata import metadata
from importlib.resources import files
from pathlib import Path
from typing import Optional

from platformdirs import user_cache_dir, user_config_dir, user_log_dir
from pydantic_settings import BaseSettings, SettingsConfigDict

from .utils import LoggingLevel, create_logger

#
#
# Get package-level information
#


# From package build metadata, possibly originating in pyproject.toml:
package_identifier: Optional[str] = __spec__.parent
if not isinstance(package_identifier, str):
    raise ValueError("Package identifier not found")
if not package_identifier.isidentifier():
    raise ValueError("Package identifier is invalid")
_package_metadata = metadata(package_identifier)
package_name: str = _package_metadata["Name"]
if package_name.replace("-", "_") != package_identifier:
    raise ValueError("Package name and package identifier mismatch")
package_version: str = _package_metadata["Version"]
system_version: str = sys.version.replace("\n", "")
package_dir = Path(files(package_identifier)).resolve()
project_dir = package_dir.parent.parent

# Platform-specific directories:
config_dir = Path(user_config_dir(package_name, ensure_exists=True)).resolve()
log_dir = Path(user_log_dir(package_name, ensure_exists=True)).resolve()
cache_dir = Path(user_cache_dir(package_name, ensure_exists=True)).resolve()


#
# Base definitions toward module-level concrete definitions
#


_logging_formatter_str = f"%(asctime)sZ - %(name)s - %(levelname)s - system {system_version} - {package_name} {package_version} - %(message)s"


def create_logger_module(
    module_name: str,
    *,
    logging_level_file: LoggingLevel = "DEBUG",
    logging_level_stderr: LoggingLevel = "WARNING",
) -> logging.Logger:
    """Create and initialize a module-level logger"""
    return create_logger(
        module_name,
        log_file=log_dir / f"{module_name}.log",
        logging_level_file=logging_level_file,
        logging_level_stderr=logging_level_stderr,
        formatter_str=_logging_formatter_str,
    )


class MyBaseSettings(BaseSettings, ABC):
    """An abstract base class to store settings"""

    model_config = SettingsConfigDict(
        env_file=config_dir / ".env",
        env_file_encoding="utf-8",
        env_prefix=f"{package_name}_",
        extra="ignore",
        frozen=True,
    )


class MyBaseSecrets(BaseSettings, ABC):
    """An abstract base class to store secrets"""

    model_config = SettingsConfigDict(
        env_file=config_dir / ".secret",
        env_file_encoding="utf-8",
        env_prefix=f"{package_name}_",
        extra="ignore",
        frozen=True,
    )
