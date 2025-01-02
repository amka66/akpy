"""
Abstract base classes for storing project information, secrets, and settings.
Concrete classes for general information and settings.
"""

from abc import ABC
from pathlib import Path

from platformdirs import user_cache_dir, user_config_dir, user_log_dir
from pydantic import BaseModel, ConfigDict, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich import print

from .read import read_toml

_root_dir = Path(__file__).parent.parent.parent.resolve()
_pyproject_toml = read_toml(_root_dir / "pyproject.toml")
_project_name: str = _pyproject_toml["project"]["name"]
_package_name = _project_name.replace("-", "_")
_version = _pyproject_toml["project"]["version"]
_env_prefix = f"{_package_name}_"

print()
_config_dir = Path(user_config_dir(_project_name, ensure_exists=True))
print(f"Configuration files must be stored at '{_config_dir}'")
print(
    f"Configuration files include '.env' and '.secret', if any, with entries of the form '{_env_prefix.upper()}VARIABLE_NAME=...'"
)
_log_dir = Path(user_log_dir(_project_name, ensure_exists=True))
print(f"Log files may be found at '{_log_dir}'")
_cache_dir = Path(user_cache_dir(_project_name, ensure_exists=True))
print(f"Cache files may be found at '{_cache_dir}'")


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
        env_file=_config_dir / ".env",
        env_file_encoding="utf-8",
        env_prefix=_env_prefix,
        extra="ignore",
        frozen=True,
    )


class MyBaseSecrets(BaseSettings, ABC):
    """An abstract base class to store project secrets"""

    model_config = SettingsConfigDict(
        env_file=_config_dir / ".secret",
        env_file_encoding="utf-8",
        env_prefix=_env_prefix,
        extra="ignore",
        frozen=True,
    )


#
# Concrete class to store general project information
#


class GeneralInfo(MyBaseInfo):
    """This class stores general information"""

    root_dir: DirectoryPath = _root_dir
    project_name: str = _project_name
    package_name: str = _package_name
    version: str = _version
    log_dir: DirectoryPath = _log_dir
    cache_dir: DirectoryPath = _cache_dir
    config_dir: DirectoryPath = _config_dir
