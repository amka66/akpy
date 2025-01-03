MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

.PHONY: pull sync clean test status recent push lock upgrade run rerun repro rerep
# .EXPORT_ALL_VARIABLES:
# .DELETE_ON_ERROR:
# .INTERMEDIATE:
# .SECONDARY:
.DEFAULT_GOAL := status

export UV_LOCKED ?= 1
export UV_NO_SYNC ?= 1
ENABLE_TESTS ?= 1
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
	@echo "Syncing dependencies..."
	uv sync --locked
# it will first create a virtual env if it doesn't exist

clean:
	@echo "Deleting temporary files..."
	find . -type f -name '.DS_Store' -delete || true
	uv run cleanpy --include-builds .
	find . -type d -name '.ipynb_checkpoints' -delete || true

ifeq ($(ENABLE_TESTS),1)
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

recent:	pull sync clean test status
# it will first create a virtual env if it doesn't exist

push: test
	@echo "Pushing file changes..."
ifeq ($(ENABLE_DVC),1)
	uv run dvc push $(RUN_CACHE)
endif
	git push

lock:
	@echo "Locking dependencies..."
	UV_LOCKED=0 uv lock

upgrade:
	@echo "Upgrading locked dependencies..."
	UV_LOCKED=0 uv lock --upgrade

run:
	@echo "Running main (args=$(ARGS))..."
	uv run $(ARGS)

rerun: recent run

ifeq ($(ENABLE_DVC),1)
repro:
	@echo "Reproducing pipeline $(PI)..."
	uv run dvc repro $(PI)

rerep: recent repro status
endif
