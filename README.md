# akpy #

> ___A blueprint for Python projects including useful definitions and utilities for Python development___

This repo is primarily for personal use.
It compiles different sources that shaped the way I work.
It is included here for public use, in case anyone finds it useful.

## Overview ##

- The repository is a Python package `akpy`, parts of which can be copied over for quickly setting up new Python projects (that is, it is intended as a blueprint for new Python projects)
- Additionally, `akpy` can be used as a standalone tool (for example, in an interactive shell, a jupyter notebook, or a standalone script) in order to access several definitions and utilities that I find useful in different scenarios
- Patterns of usage of some of these definitions is illustrated too
- It is generally less advisable to import `akpy` into other packages (rather than a standalone tool), as (a) files need to be copied over (and generally edited) for it to serve as a blueprint for other projects; and (b) definitions are not comprehensive enough (that is, they might need to be edited) or stable enough for `akpy` to be used as a serious long-term dependency

## Prerequisites ##

- To import `akpy`, install the package and all dependencies using `pip` or equivalent (`pipx`, `uv tool`, etc.) by running `pip install git+https://github.com/amka66/akpy.git` (similarly for other package managers)
- The repository was set up using `uv`, which is the recommended package manager when using `akpy` as a blueprint for other projects
- Additional functionality requires a Docker engine, the (in)famous make utility, and/or VSCode, which are optional
