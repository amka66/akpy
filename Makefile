MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

.PHONY: pull sync clean lint_light lint test status recent push reformat lock upgrade run rerun repro rerep
# .EXPORT_ALL_VARIABLES:
# .DELETE_ON_ERROR:
# .INTERMEDIATE:
# .SECONDARY:
.DEFAULT_GOAL := status

# Configure (if not set)
ENABLE_DVC ?= 0
SYNC_DVC_CACHE ?= 0

# Set default parameters (if not set)
ARGS ?= akpy
PIPE ?= dvc.yaml

# More definitions
export UV_LOCKED = 1
export UV_NO_SYNC = 1

ifeq ($(SYNC_DVC_CACHE),1)
RUN_CACHE = --run-cache
else
RUN_CACHE =
endif

#
# Rules
#

pull:
	@echo "==> Pulling file changes..."
	git fetch --all --tags
	[[ -z  "$$(git branch --format "%(upstream:short)" --list "$$(git branch --show-current)")" ]] || git merge --ff-only
ifeq ($(ENABLE_DVC),1)
	uv run dvc fetch $(RUN_CACHE)
	-uv run dvc checkout
endif

sync:
	@echo "==> Syncing dependencies from lock file..."
	uv sync
# it will first create a virtual env if it doesn't exist

clean:
	@echo "==> Deleting temporary files..."
	uv run cleanpy --include-builds .
	find . -type d -name '.ipynb_checkpoints' -delete || true
	find . -type f -name '.DS_Store' -delete || true

lint_light:
	@echo "==> Checking source files formatting..."
	uv run black --check --diff .
	uv run isort --check --diff .
	uv run ruff check .

lint: lint_light
	@echo "==> Linting source files..."
	# uv run mypy .  # skipping (failing)
	# uv run pyright .  # skipping (failing)
	# uv run pylint .  # skipping (failing)
	# uv run bandit -r . -c pyproject.toml  # skipping (failing)
# TODO: revise source files to avoid failing linters

test:
	@echo "==> Running tests..."
	uv run pytest

status:
	@echo "==> Reporting file status..."
	du -sh .
	git status
ifeq ($(ENABLE_DVC),1)
	uv run dvc status
	uv run dvc data status --granular
	uv run dvc diff
	uv run dvc params diff
	uv run dvc metrics diff
	# uv run dvc plots diff
	uv run dvc status --cloud
endif

recent:	pull sync clean lint test status
# it will first create a virtual env if it doesn't exist

push: lint test
	@echo "==> Pushing file changes..."
ifeq ($(ENABLE_DVC),1)
	uv run dvc push $(RUN_CACHE)
endif
	git push

format:
	@echo "==> Formatting source files..."
	uv run black .
	uv run isort .
	# uv run ruff format .
# to avoid inconsistencies while formatting sources files, ruff is only used in 'check' mode

lock:
	@echo "==> Resolving and locking dependencies..."
	UV_LOCKED=0 uv lock

upgrade:
	@echo "==> Upgrading locked dependencies..."
	env -u UV_LOCKED uv lock --upgrade

run:
	@echo "==> Running $(ARGS)..."
ifeq ($(ARGS),)
	$(error "Environment variable 'ARGS' is undefined or empty")
endif
	uv run $(ARGS)

rerun: recent run

ifeq ($(ENABLE_DVC),1)
repro:
	@echo "==> Reproducing $(PIPE)..."
ifndef PIPE
	$(error "Environment variable 'PIPE' is undefined")
endif
	uv run dvc repro $(PIPE)

rerep: recent repro status
endif
