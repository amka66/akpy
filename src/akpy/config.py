"""
Abstract base classes for storing project information, secrets, and settings.
Concrete classes for general information and settings.
"""

import os
from abc import ABC
from pathlib import Path
from typing import Literal

from platformdirs import user_cache_dir, user_config_dir, user_log_dir
from pydantic import BaseModel, ConfigDict, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich import print

from .read import read_toml

LoggingLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

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
    _cache_dir = _root_dir / "cache"
    os.makedirs(_cache_dir, exist_ok=True)
    _env_dir = _root_dir
else:
    _log_dir = Path(user_log_dir(_project_name, ensure_exists=True))
    print(f"Log files may be found in {_log_dir}")
    _cache_dir = Path(user_cache_dir(_project_name, ensure_exists=True))
    print(f"Cache files may be found in {_cache_dir}")
    _env_dir = Path(user_config_dir(_project_name, ensure_exists=True))
    print(f"Environment and secret files may be stored in {_env_dir}")


#
# Abstract base classes for different modules to store project information, secrets, and settings
#


class MyBaseInfo(BaseModel, ABC):
    """An abstract base class to store project information"""

    model_config = ConfigDict(
        validate_default=True,
        frozen=True,
    )


class MyBaseSettings(BaseSettings, ABC):
    """An abstract base class to store project settings"""

    model_config = SettingsConfigDict(
        env_file=_env_dir / ".env",
        env_file_encoding="utf-8",
        env_prefix=_env_prefix,
        extra="ignore",
        frozen=True,
    )


class MyBaseSecrets(BaseSettings, ABC):
    """An abstract base class to store project secrets"""

    model_config = SettingsConfigDict(
        env_file=_env_dir / ".secret",
        env_file_encoding="utf-8",
        env_prefix=_env_prefix,
        extra="ignore",
        frozen=True,
    )


#
# Concrete classes to store general project information, secrets, and settings
#


class GeneralInfo(MyBaseInfo):
    """This class stores general information"""

    root_dir: DirectoryPath = _root_dir
    project_name: str = _project_name
    package_name: str = _package_name
    version: str = _version
    is_dev_env: bool = _is_dev_env
    log_dir: DirectoryPath = _log_dir
    cache_dir: DirectoryPath = _cache_dir
    env_dir: DirectoryPath = _env_dir


class GeneralSettings(MyBaseSettings):
    """This class stores general settings"""

    logging_level: LoggingLevel = "WARNING"
