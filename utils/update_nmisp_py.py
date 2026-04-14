"""
Copy .py files from nmisp into a checked-out nmisp_py directory.

CI handles checkout and commit/push via actions/checkout + git-auto-commit-action.
This script only does the file synchronisation.

Usage:
    python update_nmisp_py.py <nmisp_py_path>
"""

import os
import pathlib
import shutil
import sys


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <nmisp_py_path>")
        sys.exit(1)

    clone_dest = pathlib.Path(sys.argv[1]).resolve()
    assert clone_dest.exists(), f"nmisp_py path does not exist: {clone_dest}"

    repo_path = get_repo_path()

    # Recursively remove all .py files in the nmisp_py repository
    for path in clone_dest.rglob("*.py"):
        os.remove(path)

    # Recursively copy all .py files into the nmisp_py repository
    for path in repo_path.rglob("*.py"):
        if path.is_relative_to(clone_dest):
            continue
        if not (
            ("tests" in path.relative_to(repo_path).parts[0:2])
            or
            ("build_util" in path.relative_to(repo_path).parts[0:2])
            or
            ("utils" == path.relative_to(repo_path).parts[0])
        ):
            print(path.relative_to(repo_path))
            shutil.copy(path, clone_dest / path.name)


def get_repo_path() -> pathlib.Path:
    """
    Get the path to the repository
    """
    util_path = pathlib.Path(__file__).parent.absolute()
    assert util_path.exists(), util_path
    assert util_path.is_dir()

    repo_path = util_path.parent.absolute()
    assert repo_path.exists(), repo_path
    assert repo_path.is_dir()
    return repo_path


if "__main__" == __name__:
    main()
