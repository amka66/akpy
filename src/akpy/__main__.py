"""
This script is executed when the package is executed with `-m`
(that is, `python -m akpy`)
"""

import sys

from . import main

sys.exit(main())
