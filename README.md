# akpy #

> ___A blueprint for Python projects including useful definitions and utilities for Python development___

This repo is primarily for personal use.
It compiles different sources from which I learned over the years that shaped the way I work.
It is included here for public use in case anyone finds it useful.

## Overview ##

- The repository is a Python package `akpy` that can be copied over for a quick set up of new packages (that is, be used as a blueprint for new Python projects)
- Additionally, `akpy` can be imported into other programs in order to access several definitions and utilities that I find useful in different scenarios (nothing fancy, a few readers / writers for common file types, handling of configuration files, maintaining secrets, logging, setting up a modern CLI, etc.)
- Patterns of usage of some of these definitions is illustrated
- Lastly, some content is available in dedicated files that may be copied over individually (a Python development environment Makefile, Dockerfile to create a relatively optimized container, VSCode settings, etc.)

## Prerequisites ##

- The repository was set up using `uv` (Python package and project manager), which is the main prerequisite to using this package as a blueprint for new projects
- Additional functionality assumes a `docker` engine, the (in)famous `make` utility, and/or `vscode`, which are optional
