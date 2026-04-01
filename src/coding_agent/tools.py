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
    ignore_dirs = {".venv", "__pycache__"}
    sandbox_root = _path_sandbox("")
    matches = sandbox_root.glob(pattern)
    return [
        str(p.relative_to(sandbox_root))
        for p in matches
        if not any(part in ignore_dirs for part in p.parts)
    ]


def delete_file(path: str) -> None:
    """Delete a file.

    Parameters
    ----------
    path : str
        The (relative) path to the file.
    """
    _path_sandbox(path).unlink()


def replace_text(path: str, old_text: str, new_text: str) -> str:
    """Replace a block of text in a file with new text.

    Parameters
    ----------
    path : str
        The (relative) path to the file.
    old_text : str
        The exact text to find and replace. Must be unique in the file.
    new_text : str
        The text to replace with.

    Returns
    -------
    str
        Success or error message.

    Notes
    -----
    - If the text is not found, returns an error message.
    - If the text appears more than once, returns an error with line numbers.
    """
    file_path = _path_sandbox(path)
    content = file_path.read_text()
    lines = content.splitlines(keepends=True)

    matches = []
    line_number = 1
    pos = 0

    while pos < len(content):
        idx = content.find(old_text, pos)
        if idx == -1:
            break
        matches.append(idx)
        pos = idx + 1

    if len(matches) == 0:
        return f"Error: text not found in {path}"
    elif len(matches) > 1:
        match_lines = []
        for match_pos in matches:
            line_num = content[:match_pos].count("\n") + 1
            match_lines.append(str(line_num))
        return f"Error: found {len(matches)} occurrences in {path} at lines: {', '.join(match_lines)}. Please provide more unique text."
    else:
        new_content = content.replace(old_text, new_text, 1)
        file_path.write_text(new_content)
        return f"Replaced 1 occurrence in {path}"
