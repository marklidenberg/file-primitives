import os

from pathlib import Path
from typing import TypeVar

T = TypeVar("T", str, Path)


def ensure_dir(
    path: T,
    is_file: bool = False,
) -> T:
    """Ensure that the directory path exists and return the path.

    Args:
        path: The directory path or file path to ensure
        is_file: If True, treats path as a file and ensures its parent directory exists
    """

    # - Get the directory to create

    if is_file:
        dirname = os.path.dirname(path)  # type: ignore
        if dirname:
            os.makedirs(dirname, exist_ok=True)
    else:
        os.makedirs(path, exist_ok=True)  # type: ignore

    return path


def test():
    ensure_dir("/tmp/ensure_directory/foo")
    ensure_dir("/tmp/ensure_directory/bar/")
    ensure_dir("/tmp/ensure_directory/bar/baz")

    assert os.path.exists("/tmp/ensure_directory/foo")
    assert os.path.exists("/tmp/ensure_directory/bar")
    assert os.path.exists("/tmp/ensure_directory/bar/baz")

    # Test is_file=True
    ensure_dir("/tmp/ensure_filepath/foo/zzz.txt", is_file=True)
    ensure_dir("/tmp/ensure_filepath/foo/bar/", is_file=True)
    ensure_dir("/tmp/ensure_filepath/foo/baz", is_file=True)

    assert os.path.exists("/tmp/ensure_filepath/foo")
    assert os.path.exists("/tmp/ensure_filepath/foo/bar")
    assert not os.path.exists("/tmp/ensure_filepath/foo/baz")


if __name__ == "__main__":
    test()
