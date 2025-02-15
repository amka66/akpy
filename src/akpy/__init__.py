"""
This module includes package-level definitions
"""

import sys

from .config import config_dir, log_dir, package_name, package_version
from .entry import main

# Import package main function
_ = main  # nop

# Set package version
__version__ = package_version

# Print package-level information
print(
    f"Configuration files of package '{package_name}' can be found at '{config_dir}'",
    file=sys.stderr,
    flush=True,
)
print(
    f"Log files of package '{package_name}' can be found at '{log_dir}'",
    file=sys.stderr,
    flush=True,
)
