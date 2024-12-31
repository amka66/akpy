"""
This module includes package-level definitions
"""

from .config import GeneralInfo
from .entry import main

# Package version
__version__ = GeneralInfo().version

# Package main function
_ = main  # nop - to avoid unused import warning
