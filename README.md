# akpy #

___A blueprint for Python projects including useful definitions and utilities for Python development___

> This repo is primarily for personal use.
> It compiles different sources that shaped the way I work.
> It is included here for public use, in case anyone finds it useful.

## Overview ##

- This repository includes a Python package `akpy`, which can be used in several ways:
    * It can serve as a **blueprint** for new Python projects -- clone or download the repository and copy over parts of it for quickly setting up a new Python project.
    * It can serve as a **library** including useful definitions and utilities -- install the package in a Python environment and import it during an interactive Python session, in a Jupyter notebook, or in a Python script.
    * In the future, it may serve as a standalone Python **application** (tool) -- install the package in a possibly isolated Python environment and invoke it during an interactive session with the operating-system's shell or in an shell script.
- It is generally *not* advisable to announce `akpy` as a dependency of other packages, as (a) for simplicity, most of the content is facilitated by copying over files rather than importing; and (b) definitions are generally not comprehensive enough (they might need to be edited) or stable enough for `akpy` to be used as a serious long-term dependency.
- Patterns of usage of `akpy` are illustrated in a demo application included as part of the package (a packaged application).

## Getting Started ##

### Blueprint ###

1. Clone the repository, e.g., by running
```
$ git clone https://github.com/amka66/akpy.git
```
2. Copy over the relevant files.
3. Edit the files as needed.

Because `akpy` was set up using [`uv`](https://docs.astral.sh/uv/) -- it is the recommended package manager for the cloned project too.
Also note that the repo includes development environment settings; particularly, `git`, `VSCode`, `make`, `DVC`, etc.

### Library ###

1. Install the package in Python environment using a package manager such as [`pip`](https://pip.pypa.io/en/stable/) or `uv`, e.g., by running
```
$ pip install git+https://github.com/amka66/akpy.git
```
or
```
$ uv add git+https://github.com/amka66/akpy.git
```
2. In Python, import the package (`import akpy`) or parts of it.

### Application ###

1. Install the package in a possibly isolated Python environment using a package manager such as [`pipx`](https://pipx.pypa.io/stable/) or `uv`, e.g., by running
```
$ pipx install git+https://github.com/amka66/akpy.git
```
or
```
$ uv tool install git+https://github.com/amka66/akpy.git
```
2. To run it, type `akpy` in the OS shell.
