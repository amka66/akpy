"""
This module includes package-level definitions
"""

from .config import (
    cache_dir,
    config_dir,
    create_logger_module,
    log_dir,
    package_name,
    package_version,
)
from .entry import main

# Import package main function
_ = main  # nop

# Set package version
__version__ = package_version

# Print package-level information
print(
    f"Configuration files of package '{package_name}' can be found in folder '{config_dir}'",
    flush=True,
)
print(
    f"Log files of package '{package_name}' can be found in folder '{log_dir}'",
    flush=True,
)

# Log package-level information
_logger = create_logger_module(__name__)

_logger.info("Configuration files in %s", config_dir)
_logger.info("Log files in %s", log_dir)
_logger.info("Cache files in %s", cache_dir)
