# akpy #

> ___A blueprint for Python projects including useful definitions and utilities for Python development___

This repo is primarily for personal use.
It compiles different sources that shaped the way I work.
It is included here for public use, in case anyone finds it useful.

## Overview ##

- The repository is a Python package `akpy` that can be copied over for quickly setting up new Python projects (that is, it is intended as a blueprint for new Python projects)
- Additionally, `akpy` can be imported into other programs in order to access several definitions and utilities that I find useful in different scenarios (nothing fancy, several reader / writer functions for common file types, a useful way to handle environment configuration files and secrets using Pydantic, setting up loggers, automatic setup of CLI from python type hints using Typer, etc.)
- Patterns of usage of some of these definitions is illustrated
- Lastly, some content is available in dedicated files that may be copied over individually (a Python development environment Makefile, VSCode settings, etc.)

## Prerequisites ##

- To import the package and automatically install all dependencies run `pip install git+https://github.com/amka66/akpy.git`
- The repository was set up using `uv` (a Python package and project manager), which is the main prerequisite to using this package as a blueprint for new projects
- Additional functionality requires a Docker engine, the (in)famous make utility, and/or VSCode, which are optional
