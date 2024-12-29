"""
Abstract base classes for storing project information, secrets, and settings.
Concrete classes for general information and settings.
"""


#
# IMPORTS
#
#

import os
from abc import ABC
from pathlib import Path
from typing import Literal

from platformdirs import user_config_dir, user_log_dir
from pydantic import BaseModel, ConfigDict, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich import print

from .read import read_toml

#
#
# TYPE HINTS
#


LoggingLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


#
# INITIALIZATION
#


_root_dir = Path(__file__).parent.parent.parent.resolve()
_pyproject_toml = read_toml(_root_dir / "pyproject.toml")
_project_name: str = _pyproject_toml["project"]["name"]
_package_name = _project_name.replace("-", "_")
_version = _pyproject_toml["project"]["version"]
_env_prefix = f"{_package_name}_"

_is_dev_env = (_root_dir / ".dev").is_file()
if _is_dev_env:
    _log_dir = _root_dir / "logs"
    os.makedirs(_log_dir, exist_ok=True)
    _env_dir = _root_dir
else:
    _log_dir = Path(user_log_dir(_project_name))
    os.makedirs(_log_dir, exist_ok=True)
    print(f"Logs may be found in {_log_dir}")
    _env_dir = Path(user_config_dir(_project_name))
    os.makedirs(_env_dir, exist_ok=True)
    print(f"Environment and secret files may be stored in {_env_dir}")


#
# STORING PROJECT INFORMATION
#


class MyBaseInfo(BaseModel, ABC):
    model_config = ConfigDict(
        validate_default=True,
    )


class GeneralInfo(MyBaseInfo):
    root_dir: DirectoryPath = _root_dir
    project_name: str = _project_name
    package_name: str = _package_name
    version: str = _version
    is_dev_env: bool = _is_dev_env
    log_dir: DirectoryPath = _log_dir
    env_dir: DirectoryPath = _env_dir


#
# STORING PROJECT SECRETS
#


class MyBaseSecrets(BaseSettings, ABC):
    model_config = SettingsConfigDict(
        env_file=_env_dir / ".secret",
        env_file_encoding="utf-8",
        env_prefix=_env_prefix,
        extra="ignore",
    )


#
# STORING PROJECT SETTINGS
#


class MyBaseSettings(BaseSettings, ABC):
    model_config = SettingsConfigDict(
        env_file=_env_dir / ".env",
        env_file_encoding="utf-8",
        env_prefix=_env_prefix,
        extra="ignore",
    )


class GeneralSettings(MyBaseSettings):
    logging_level: LoggingLevel = "WARNING"
