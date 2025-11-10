from pathlib import Path
from typing import Union
import shutil

from file_primitives.write_file import write_file


def delete_path(
    path: Union[str, Path],
    missing_ok: bool = False,
    delete_empty_parents: bool = False,
) -> bool:
    """Delete a file or directory at the specified path.

    Args:
        path: The path to delete
        missing_ok: If True, don't raise an error if the path doesn't exist
        delete_empty_parents: If True, also remove empty parent directories

    Returns:
        True if the path was deleted, False if it didn't exist (when missing_ok=True)
    """
    # - Convert path to Path

    path = Path(path)

    # - Get absolute path

    path = path.absolute()

    # - Delete target

    def _delete() -> bool:
        # - Try to remove target as a directory

        try:
            shutil.rmtree(path)
            return True
        except FileNotFoundError:
            if not missing_ok:
                raise FileNotFoundError(f"Path {path} not found")
            return False
        except NotADirectoryError:
            pass

        # - Try to remove target as a file or symlink

        try:
            path.unlink(missing_ok=missing_ok)
            return True
        except FileNotFoundError:
            return False
        except IsADirectoryError:
            # a directory has become a file in the meantime, just do nothing
            return False

    deleted = _delete()

    # - Cleanup empty parents

    if delete_empty_parents and deleted:
        for parent in path.parents:
            try:
                parent.rmdir()
            except OSError:
                break

    return deleted


def test():
    write_file(path="output/test.txt", data="test")
    result = delete_path(path="output/test.txt")
    assert result is True


if __name__ == "__main__":
    test()
