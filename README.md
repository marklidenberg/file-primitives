# file-primitives

Python file primitives

* `read_file`: reads file with an option to specify default if file does not exist or a custom reader (like `reader = lambda file: json.read(file)`)
* `write_file`: writes file with auto-directory creation, custom writer, and optional atomic writes
* `ensure_dir`: ensures a directory exists
* `delete_path`: deletes a file or directory. Returns `bool` indicating success.

```python
def read_file(
    path: Union[str, Path],
    bytes: bool = False,
    reader: Callable[..., T] = lambda file: file.read(),
    default: Union[D, object] = MISSING,  # if file does not exist
    encoding: str = "utf-8",
) -> Union[T, D]:
    pass

def write_file(
    path: Union[str, Path],
    data: T,
    bytes: bool = False,
    writer: Callable[[T, Any], Any] = lambda data, file: file.write(data),
    encoding: str = "utf-8",
    ensure_dir: bool = True,
    atomic: bool = False,
) -> None:
    pass

def ensure_dir(
    path: T,  # T = TypeVar("T", str, Path)
    is_file: bool = False,
) -> T:
    pass

def delete_path(
    path: Union[str, Path],
    missing_ok: bool = False,
    delete_empty_parents: bool = False,
) -> bool:
    pass

...

from file_primitives import read_file, write_file, ensure_dir, delete_path

# Simple file operations
content = read_file("config.json")

# Binary mode
binary_content = read_file("image.png", bytes=True)

# output dir will be created automatically
write_file("output/data.json", {"key": "value"}, writer=lambda data, file: json.dump(data, file))

# Atomic write (prevents corruption)
write_file("important.json", data, atomic=True)

# With error handling
config = read_file("missing.json", default="I am missing")

ensure_dir("logs/2024/january")  # Creates full path
ensure_dir("reports/summary.pdf", is_file=True)  # Creates "reports/" directory

# Delete operations
deleted = delete_path("temp/file.txt")  # Returns True if deleted, False if not found (with missing_ok=True)
```