MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

.PHONY: pull sync clean lint test status recent push reformat lock upgrade run rerun repro rerep
# .EXPORT_ALL_VARIABLES:
# .DELETE_ON_ERROR:
# .INTERMEDIATE:
# .SECONDARY:
.DEFAULT_GOAL := status

export UV_LOCKED ?= 1
export UV_NO_SYNC ?= 1
ENABLE_FORMATTING ?= 1
ENABLE_LINTING ?= 1
ENABLE_TESTING ?= 1
ENABLE_DVC ?= 0
SYNC_DVC_CACHE ?= 0

ARGS ?= akpy
PI ?= dvc.yaml

ifeq ($(SYNC_DVC_CACHE),1)
RUN_CACHE = --run-cache
else
RUN_CACHE =
endif

pull:
	@echo "Pulling file changes..."
	git fetch --all --tags
	[[ -z  "$$(git branch --format "%(upstream:short)" --list "$$(git branch --show-current)")" ]] || git merge --ff-only
ifeq ($(ENABLE_DVC),1)
	uv run dvc fetch $(RUN_CACHE)
	-uv run dvc checkout
endif

sync:
	@echo "Syncing dependencies from lock file..."
	uv sync
# it will first create a virtual env if it doesn't exist

clean:
	@echo "Deleting temporary files..."
	uv run cleanpy --include-builds .
	find . -type d -name '.ipynb_checkpoints' -delete || true
	find . -type f -name '.DS_Store' -delete || true


ifeq ($(ENABLE_LINTING),1)
lint:
	@echo "Checking and linting source files..."
	uv run black --check --diff .
	uv run isort --check --diff .
	uv run ruff check .
	uv run mypy .
	uv run pyright .
	uv run pylint .
	uv run bandit -r . -c pyproject.toml
endif

ifeq ($(ENABLE_TESTING),1)
test:
	@echo "Running tests..."
	uv run pytest
endif

status:
	@echo "Reporting file status..."
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
	@echo "Pushing file changes..."
ifeq ($(ENABLE_DVC),1)
	uv run dvc push $(RUN_CACHE)
endif
	git push

ifeq ($(ENABLE_FORMATTING),1)
reformat:
	@echo "Formatting source files..."
	uv run black .
	uv run isort .
	uv run ruff format .
endif

lock:
	@echo "Resolving and locking dependencies..."
	UV_LOCKED=0 uv lock

upgrade:
	@echo "Upgrading locked dependencies..."
	UV_LOCKED=0 uv lock --upgrade

run:
	@echo "Running $(ARGS)..."
	uv run $(ARGS)

rerun: recent run

ifeq ($(ENABLE_DVC),1)
repro:
	@echo "Reproducing $(PI)..."
	uv run dvc repro $(PI)

rerep: recent repro status
endif
