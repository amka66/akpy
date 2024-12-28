# akpy #

> This repo is primarily for personal use.
> It compiles material I read over the years, which shaped the way I work.
> It is included here for public use in case it may help anyone set up their development environment more to their liking.

## Overview ##

- The repository is a Python package `akpy` that can be copied over for a quick set up of new packages (that is, be used as a blueprint for new Python projects)
- Additionally, `akpy` can be imported into other programs in order to access several definitions and utilities that I find useful in different scenarios (nothing fancy, a few readers / writers for common file types, handling of configuration files, maintaining secrets, logging, setting up a modern CLI, etc.)
- Patterns of usage of some of these definitions is illustrated
- Lastly, some content is available in dedicated files that may be copied over individually (a Python development environment Makefile, Dockerfile to create a relatively optimized container, VSCode settings, etc.)

## Prerequisites ##

- The repository was set up using `uv` (Python package and project manager), which is the main prerequisite to using this package as a blueprint for new projects
- Additional functionality assumes a `docker` engine, the (in)famous `make` utility, and/or `vscode`, which are optional

## Details Stored for Future Reference ##

The package was initially created by essentially the following sequence (before it was supplemented with more content):

```
uv init --app --package --python 3.12 --python-preference only-managed akpy
cd akpy
git add .
git commit -m "Initialize a packaged python app using uv"
uv python install 3.12
uv venv
uv add openai tiktoken ipykernel nest-asyncio "typer" pydantic pydantic-settings \
    platformdirs cleanpy numpy pandas annotated-types typeguard "nptyping[complete]" \
    jsonlines jsonpickle toml pyyaml matplotlib pytest torch torchvision torchaudio \
    scipy transformers "datasets[audio,vision]" evaluate "httpx[cli,http2]" "fastapi[all]"
git add .
git commit -m "Install python, create venv, add dependencies"
```
