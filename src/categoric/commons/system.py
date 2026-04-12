import datetime
import hashlib
import pathlib
import uuid


def temp_dir(
    work_dir: pathlib.Path,
    prefix: str = "tmp",
    nested: bool = False,
    create: bool = True,
    mode: int = 0o755,
) -> pathlib.Path:
    """Create a temporary directory with a unique name.

    Args:
        work_dir: The base directory where the temporary directory will be created.
        prefix: Prefix for the directory name.
        nested: If True, uses a date-based nested structure (YYYY/MM/DD/HHMM_f).
        create: If True, creates the directory on the file system.
        mode: Permissions for the created directory.

    Returns:
        The path to the created temporary directory.

    """
    # FIXME: CVE-2025-71176 https://github.com/pytest-dev/pytest/issues/13669

    rand_uuid = uuid.uuid4().hex.lower()
    if nested:
        now = datetime.datetime.now(datetime.UTC).strftime("%Y/%m/%d/%H%M_%f")
    else:
        now = datetime.datetime.now(datetime.UTC).strftime("_%Y%m%d_%H%M_%f")
    tmp_path = work_dir.joinpath(f"{prefix}{now}_{rand_uuid[:8]}")
    if create:
        tmp_path.mkdir(mode=mode, parents=True, exist_ok=True)
    return tmp_path


def temp_file(
    work_dir: pathlib.Path,
    prefix: str = "",
    suffix: str = ".out",
    create: bool = True,
    dir_mode: int = 0o755,
    file_mode: int = 0o644,
) -> pathlib.Path:
    """Create a temporary file with a unique name.

    Args:
        work_dir: The base directory where the temporary file will be created.
        prefix: Prefix for the file name.
        suffix: Suffix (extension) for the file name.
        create: If True, creates the directory and the file.
        dir_mode: Permissions for the created directory.
        file_mode: Permissions for the created file.

    Returns:
        The path to the temporary file.

    """
    rand_uuid = uuid.uuid4().hex.lower()
    now = datetime.datetime.now(datetime.UTC).strftime("%Y/%m/%d/%H%M_%f")
    tmp_file = work_dir.joinpath(f"{prefix}{now}_{rand_uuid[:8]}{suffix}")
    if create:
        work_dir.mkdir(mode=dir_mode, parents=True, exist_ok=True)
        tmp_file.touch(mode=file_mode, exist_ok=True)
    return tmp_file


def md5sum(data: str) -> str:
    """Calculate the MD5 checksum of a string.

    Args:
        data: The input string to hash.

    Returns:
        The hex-encoded MD5 hash.

    """
    return hashlib.md5(data.encode("utf-8"), usedforsecurity=False).hexdigest()
