"""This file contains utility functions for operation on file paths."""

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import hashlib
import inspect
import os
import re
import sys
import time
from collections.abc import Callable
from types import ModuleType
from typing import Any


def config_file(relative_file_path: str) -> str:
    """Returns a path to file located in {test_name}_data directory, where
    {test_name} is name of the test module that called this function.
    example: using test_utils.config_file('my_file') in my_test.py will return
    'tests/my_test_data/my_file'
    """
    caller = inspect.stack()[1]
    caller_mod = inspect.getmodule(caller[0])
    if caller_mod is None:
        raise RuntimeError("Unable to determine caller module")
    caller_mod_file_path = caller_mod.__file__
    if caller_mod_file_path is None:
        raise RuntimeError(f"Module {caller_mod.__name__} has no __file__ attribute")
    return f"{caller_mod_file_path.rstrip(".py")}_data/{relative_file_path}"


def get_file_name(file_path: str) -> str:
    """Returns name of file, based on file_path.
    Name is acquired by removing parent directories from file_path and stripping
    extension.
    i.e. get_file_name("dir1/dir2/file.py") will return "file"
    """
    return os.path.splitext(os.path.basename(file_path))[0]


def get_logdir_name(root_dir: str, test_name: str) -> str:
    """Returns path to logs directory
    i.e. get_logdir_name("tests/mytest", "test1") will return
    "tests/mytest/test1.<timestamp>"
    """
    timestamp = str(time.time())
    return os.path.join(root_dir, ".".join([test_name, timestamp]))


def make_logdir(root_dir: str | None, test_name: str) -> str:
    """Creates logdir if it doesn't exist."""
    if root_dir is None:
        raise ValueError("Root directory cannot be None")
    name = get_logdir_name(root_dir, test_name)
    if not os.path.exists(name):
        os.makedirs(name)
    return name


def get_json_files(directory: str, relative: bool = False) -> list[str]:
    """Gets all .json files from given directory
    Returns list of files' absolute paths"""
    jsons = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            if not relative:
                jsons.append(os.path.join(directory, file))
            else:
                jsons.append(file)
    return jsons


def save_log_to_file(file_path: str, log: str) -> None:
    """Saves log to file pointed by file_path"""
    with open(file_path, "w") as f:
        f.write(log)


def append_log_to_file(path: str, log: str) -> None:
    """Appends log to file pointed by path"""
    with open(path, "a") as f:
        f.write(f"{log}\n\n")
        os.utime(path, None)


def get_module(name: str) -> ModuleType:
    """Returns module object"""
    return sys.modules[name]


def get_function(module: ModuleType, function_name: str) -> Callable[..., Any]:
    """Returns function object from given module"""
    return getattr(module, function_name)


def ensure_json(file: str) -> str:
    """Ensures that file has .json extension."""
    if os.path.splitext(file)[1] != ".json":
        file = ".".join([file, "json"])
    return file


def ensure_yaml(file: str) -> str:
    """Ensures that file has .yaml extension."""
    if os.path.splitext(file)[1] != ".yaml":
        file = ".".join([file, "yaml"])
    return file


def absolute_path_to_env_file(directory: str | None, file: str) -> str:
    """Returns absolute path to environment file from dir. Ensures that file
    has .yaml extension"""
    if directory is None:
        raise ValueError("Environment file directory cannot be None")
    return os.path.join(directory, ensure_yaml(file))


def escape_path(path: str) -> str:
    """Returns path with escaped space and apostrophe"""
    return path.replace("'", "\\'").replace(" ", r"\ ")


def get_first_path_element(path: str) -> str:
    """Returns first element in path"""
    return next(elem for elem in path.split(os.path.sep) if elem)


def build_test_dir_name(node: Any, max_length: int = 180) -> str:
    """
    Build a filesystem-safe directory name from pytest nodeid
    consisting of: test name + parameters + full name test hash
    full name test hash is added to ensure uniqueness test dir names
    whole name has max max_length characters.
    """

    nodeid = node.nodeid
    original_name = getattr(node, "originalname", None) or node.name
    all_name = node.name

    # remove prefix test from head
    head = original_name.removeprefix("test_")
    tail = all_name[len(original_name) :]

    # shorten too long tail
    if len(tail) > max_length * (2 / 3):
        tail = tail[: (max_length * 2) // 3]

    hash_digest = hashlib.blake2s(
        nodeid.encode("utf-8"),
        digest_size=6,
    ).hexdigest()[:8]

    head_len = max_length - len(tail) - len(hash_digest) - 2
    test_dir_name = f"{head[:head_len]}_{tail}_{hash_digest}"

    test_dir_name = re.sub(r"[^a-zA-Z0-9._-]+", "_", test_dir_name)
    test_dir_name = re.sub(r"_+", "_", test_dir_name)

    if len(test_dir_name) > max_length:
        print(
            "Applying extra shortening, because test dir name is still too long:"
            f" {test_dir_name}"
        )
        test_dir_name = test_dir_name[:max_length]

    return test_dir_name
