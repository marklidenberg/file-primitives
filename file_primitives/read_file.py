import os.path

from pathlib import Path
from typing import Callable, TypeVar, Union, overload

# Sentinel value for default parameter
MISSING = object()

T = TypeVar("T")
D = TypeVar("D")


@overload
def read_file(
    path: Union[str, Path],
    bytes: bool = False,
    reader: Callable[..., T] = lambda file: file.read(),
    *,
    encoding: str = "utf-8",
) -> T: ...


@overload
def read_file(
    path: Union[str, Path],
    bytes: bool = False,
    reader: Callable[..., T] = lambda file: file.read(),
    default: D = ...,
    encoding: str = "utf-8",
) -> Union[T, D]: ...


def read_file(
    path: Union[str, Path],
    bytes: bool = False,
    reader: Callable[..., T] = lambda file: file.read(),
    default: Union[D, object] = MISSING,  # if file does not exist
    encoding: str = "utf-8",
) -> Union[T, D]:
    # - Check if file exists

    if not os.path.exists(path) and default is not MISSING:
        return default  # type: ignore

    # - Read file

    with open(
        path,
        mode="rb" if bytes else "r",
        encoding=encoding if not bytes else None,
    ) as file:
        return reader(file)


def test():
    assert (
        read_file(
            path=__file__,
        )[:6]
        == "import"
    )
    assert (
        read_file(
            path=__file__,
            bytes=True,
        )[:6]
        == b"import"
    )


if __name__ == "__main__":
    test()
