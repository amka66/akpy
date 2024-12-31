"""
Functions for reading all sorts of data files.

All functions must conform to the type `Callable[[Path], Any]`,
possibly including more parameters (and possibly a specialization
of this type).
"""

import json
import pickle
from pathlib import Path
from typing import Any, List

import jsonlines
import jsonpickle
import numpy as np
import pandas as pd

# import tomllib
import toml
import yaml

#
#
# Functions for reading from different file formats
#


def read_text(file: Path) -> str:
    """Read text file (typically, *.txt)"""
    with open(file, "r", encoding="utf-8") as f_d:
        return f_d.read()


def read_lines(file: Path) -> List[str]:
    """Read text file line-by-line (may use extension *.txtl)"""
    with open(file, "r", encoding="utf-8") as f_d:
        return [line.rstrip("\n") for line in f_d]


def read_json(file: Path) -> Any:
    """Read JSON file (typically, *.json)"""
    with open(file, "r", encoding="utf-8") as f_d:
        return json.load(f_d)


def read_yaml(file: Path, **kwargs: Any) -> Any:
    """Read YAML file (typically, *.yaml)"""
    with open(file, "r", encoding="utf-8") as f_d:
        return yaml.safe_load(f_d, **kwargs)


def read_toml(file: Path, **kwargs: Any) -> dict[str, Any]:
    """Read TOML file (typically, *.toml)"""
    # with open(file, "rb") as f_d:
    #     return tomllib.load(f_d, **kwargs)
    return toml.load(file, **kwargs)


def read_jsonlines(file: Path) -> List[Any]:
    """Read JSONLINES file (typically, *.jsonl)"""
    with jsonlines.open(file, "r") as f_reader:
        return [obj for obj in f_reader]


def read_jsonlines_to_dataframe(file: Path) -> pd.DataFrame:
    """Read JSONLINES file and transform it into a dataframe (may use extension *.df.jsonl)"""
    return pd.read_json(file, orient="records", lines=True, encoding="utf-8")


def read_csv(
    file: Path, *, sep: str = ",", index_col=None, **kwargs: Any
) -> pd.DataFrame:
    """Read CSV file as a dataframe (typically, *.csv)"""
    return pd.read_csv(file, encoding="utf-8", sep=sep, index_col=index_col, **kwargs)


def read_tsv(file: Path, **kwargs: Any) -> pd.DataFrame:
    """Read TSV file as a dataframe (typically, *.tsv)"""
    return read_csv(file, sep="\t", **kwargs)


def read_nptxt_int64(
    file: Path,
) -> np.ndarray[np.dtype[np.int64], np.dtype[np.int64]]:
    """Read integer numpy array file (may use extension *.int64.nptxt)"""
    return np.loadtxt(file, dtype=np.int64, encoding="utf-8")


def read_nptxt_float64(
    file: Path,
) -> np.ndarray[np.dtype[np.float64], np.dtype[np.float64]]:
    """Read floating-point numpy array file (may use extension *.float64.nptxt)"""
    return np.loadtxt(file, dtype=np.float64, encoding="utf-8")


def read_pickle(file: Path, *, trusted: bool = False) -> Any:
    """
    Read pickle file (typically, *.pickle)
    NOTE It is generally unsafe and should only be used if the file is trusted!
    """
    if not trusted:
        raise ValueError("Untrusted pickle file")
    with open(file, "br") as f_d:
        return pickle.load(f_d)


def read_jsonpickle(file: Path, *, trusted: bool = False, **kwargs: Any) -> Any:
    """
    Read JSONPICKLE file (may use extension *.pickle.json)
    NOTE It is generally unsafe and may only be used if the file is trusted!
    """
    if not trusted:
        raise ValueError("Untrusted JSONPICKLE file")
    # return jsonpickle.decode(read_text(file), **kwargs)
    unpickler = jsonpickle.unpickler.Unpickler(**kwargs)
    return unpickler.restore(read_json(file))


def read_jsonlinespickle(
    file: Path, *, trusted: bool = False, **kwargs: Any
) -> List[Any]:
    """
    Read JSONLINESPICKLE file (may use extension *.pickle.jsonl)
    NOTE It is generally unsafe and may only be used if the file is trusted!
    """
    if not trusted:
        raise ValueError("Untrusted JSONLINESPICKLE file")
    # def decode(encoded: str) -> Any:
    #     return jsonpickle.decode(encoded, **kwargs)
    # return list(map(decode, read_lines(file)))
    unpickler = jsonpickle.unpickler.Unpickler(**kwargs)
    return list(map(unpickler.restore, read_jsonlines(file)))
