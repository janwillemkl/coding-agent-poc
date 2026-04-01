from pathlib import Path


def _path_sandbox(path: str) -> Path:
    return Path("sandbox") / Path(path)


def read_file(path: str) -> str:
    """Read the contents of a file

    Parameters
    ----------
    path : str
        The (relative) path to the file.

    Returns
    -------
    str
        The contents of the file.
    """
    return _path_sandbox(path).read_text()


def write_file(path: str, content: str) -> None:
    """Write contents to a file.

    Parameters
    ----------
    path : str
        The (relative) path to the file.
    content : str
        The contents to be written to the file.
    """
    file_path = _path_sandbox(path)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)


def search_files(pattern: str) -> list[str]:
    """Search for files matching a glob pattern.

    Parameters
    ----------
    pattern : str
        The glob pattern to match files (e.g., '**/*.py', 'test_*.py').

    Returns
    -------
    list[str]
        A list of relative paths matching the pattern.
    """
    sandbox_root = _path_sandbox("")
    matches = sandbox_root.glob(pattern)
    return [str(p.relative_to(sandbox_root)) for p in matches]
