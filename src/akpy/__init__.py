"""
This module includes package-level definitions
"""

from .config import package_version
from .entry import main

# Package version
__version__ = package_version

# Package's main function
_ = main  # nop - to avoid unused import warning
