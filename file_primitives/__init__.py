from importlib.metadata import version

try:
    __version__ = version("file-primitives")
except Exception:
    __version__ = "unknown"

from .read_file import read_file
from .write_file import write_file
from .ensure_dir import ensure_dir
from .delete_path import delete_path

__all__ = [
    "__version__",
    "read_file",
    "write_file",
    "ensure_dir",
    "delete_path",
]
