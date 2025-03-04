"""
This module includes utility functions and related definitions
"""

import logging
import os
import random
import string
import sys
import time
from itertools import zip_longest
from pathlib import Path
from typing import Any, Iterable, Literal, Union

int0 = int  # type hint to denote integer >= 0
LoggingLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def create_logger(
    name: str,
    *,
    log_file: Union[str, Path],
    logging_level_file: LoggingLevel = "DEBUG",
    logging_level_stderr: LoggingLevel = "WARNING",
    formatter_str: str = "%(asctime)sZ - %(name)s - %(levelname)s - %(message)s",
) -> logging.Logger:
    """
    Create and initialize a logger
    """
    log_file = Path(log_file)
    formatter = logging.Formatter(formatter_str)
    formatter.converter = time.gmtime
    logger = logging.getLogger(name)
    os.makedirs(log_file.parent, exist_ok=True)
    file_log_handler = logging.FileHandler(
        log_file,
        mode="a",
        encoding="utf-8",
        delay=False,
    )
    file_log_handler.setFormatter(formatter)
    file_log_handler.setLevel(logging_level_file)
    logger.addHandler(file_log_handler)
    stderr_log_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_log_handler.setFormatter(formatter)
    stderr_log_handler.setLevel(logging_level_stderr)
    logger.addHandler(stderr_log_handler)
    logger.setLevel(logging.DEBUG)  # ensures that handler logging levels effect
    return logger


def generate_random_string(length: int0) -> str:
    """Generate a random string including lowercase letters, uppercase letters, and digits"""
    letters = string.ascii_letters + string.digits
    result_str = "".join(random.choice(letters) for _ in range(length))
    return result_str


def compare_iterables(iterable1: Iterable[Any], iterable2: Iterable[Any]) -> bool:
    """
    Compares pairs of elements of two iterables iteratively to avoid loading
    all elements at once
    """
    sentinel = object()
    return all(
        (a == b and a is not sentinel and b is not sentinel)
        for a, b in zip_longest(iterable1, iterable2, fillvalue=sentinel)
    )
