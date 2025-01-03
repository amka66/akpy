"""
This script is executed when the package is executed with `-m` (that is, `python -m package_name`)
"""

import sys

from . import main

sys.exit(main())
