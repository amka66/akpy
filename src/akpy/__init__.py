#
# IMPORTS
#


from .config import GeneralInfo

#
#
# INITIALIZATION
#


__version__ = GeneralInfo().version


#
# MAIN
#


def main() -> None:
    print(f"Hello from akpy (version {__version__})!")
