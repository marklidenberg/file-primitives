import os
import tempfile

from pathlib import Path
from typing import Any, Callable, TypeVar, Union

from file_primitives.ensure_dir import ensure_dir as _ensure_dir

T = TypeVar("T")


def write_file(
    path: Union[str, Path],
    data: T,
    bytes: bool = False,
    writer: Callable[[T, Any], Any] = lambda data, file: file.write(data),
    encoding: str = "utf-8",
    ensure_dir: bool = True,
    atomic: bool = False,
) -> None:
    """A simple file writer helper, as it should have been in the first place. Useful for one-liners or nested function calls."""

    # - Ensure path

    if ensure_dir:
        _ensure_dir(path, is_file=True)  # type: ignore

    # - Atomic write

    if atomic:
        # Write to a temporary file first, then rename (atomic operation)
        _path = Path(path)
        file_descriptor, temp_path = tempfile.mkstemp(
            dir=_path.parent,
            prefix=f".{_path.name}.",
            suffix=".tmp",
        )
        try:
            # - Write

            with os.fdopen(
                file_descriptor,
                mode="wb" if bytes else "w",
                encoding=encoding if not bytes else None,
            ) as file:
                writer(data, file)

            # - Atomic rename

            os.replace(temp_path, path)
        except Exception:
            # Clean up temp file on error
            try:
                os.unlink(temp_path)
            except Exception:
                pass
            raise

        return

    # - Write file

    with open(
        path,
        mode="wb" if bytes else "w",
        encoding=encoding if not bytes else None,
    ) as file:
        writer(data, file)


def test():
    filename = "test.txt"
    data = "test"
    write_file(
        path=filename,
        data=data,
    )

    assert open(filename, "r").read() == data

    os.remove(filename)


if __name__ == "__main__":
    test()
