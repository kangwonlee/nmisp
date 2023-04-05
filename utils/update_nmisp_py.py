"""
This script is used to update the nmisp_py repository with the latest changes
"""

import os
import pathlib
import shutil
import subprocess
import tempfile


def main():

    repo_path = get_repo_path()

    # get current branch name
    current_branch = subprocess.check_output(
        ["git", "branch", "--show-current"],
        cwd=repo_path,
    ).decode("utf-8").strip()

    repo_name = "nmisp_py"
    org_name = "kangwonlee"
    LOGIN_INFO = os.environ["LOGIN_INFO"]

    # Checkout nmisp_py repository into a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        clone_dest = pathlib.Path(temp_dir) / repo_name
        assert not clone_dest.exists()

        # add LOGIN_INFO
        # Github repository / Settings / Secrets and variables / Actions / Repository secrets
        subprocess.check_call(
            ["git", "clone", f"https://github-actions:{LOGIN_INFO}@github.com/{org_name}/{repo_name}", os.fspath(clone_dest.absolute())],
        )

        assert clone_dest.exists()

        branch_business(clone_dest, current_branch)

        # Recursively remove all .py files in the cloned repository
        for path in clone_dest.rglob("*.py"):
            os.remove(path)

        # Recursively copy all .py files into the nmisp_py repository
        for path in repo_path.rglob("*.py"):
            if path.relative_to(clone_dest).parts[0] not in ("tests", "utils"):
                shutil.copy(path, clone_dest / path.name)

        # Commit and push the changes to the nmisp_py repository
        subprocess.check_call(
            ["git", "config", "user.name", "github-actions"],
            cwd=clone_dest,
        )
        subprocess.check_call(
            ["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"],
            cwd=clone_dest,
        )

        # Commit and push the changes to the nmisp_py repository
        subprocess.check_call(
            ["git", "add", "."],
            cwd=clone_dest,
        )

        subprocess.check_call(
            ["git", "commit", "-m", "Update nmisp_py"],
            cwd=clone_dest,
        )

        subprocess.check_call(
            ["git", "push"],
            cwd=clone_dest,
        )

    # Remove the temporary directory


def branch_business(clone_dest, current_branch:str):
    """
    Check if the current branch exists in the cloned repository.
    If it exists, checkout that branch.
    Otherwise, create a new branch.
    """

    # get the name of the branch of the cloned repository
    current_cloned_branch = subprocess.check_output(
        ["git", "branch", "--show-current"],
        cwd=clone_dest,
        encoding="utf-8",
    ).strip()

    if current_cloned_branch != current_branch:
        # get the list of all branches of the cloned repository
        branches = subprocess.check_output(
            ["git", "branch", "--all"],
            cwd=clone_dest,
            encoding="utf-8",
        ).splitlines()

        # get the list of names of all branches of the cloned repository
        branch_names = ['/'.join(branch.strip().split("/")[2:]) for branch in branches]

        # if the current branch exists in the cloned repository, checkout that branch
        if current_branch in branch_names:
            subprocess.check_call(
                ["git", "switch", current_branch],
                cwd=clone_dest,
            )
        else:
            # otherwise, create a new branch
            subprocess.check_call(
                ["git", "switch", "-c", current_branch],
                cwd=clone_dest,
            )


def get_repo_path() -> pathlib.Path:
    """
    Get the path to the repository
    """
    util_path = pathlib.Path(__file__).parent.absolute()
    assert util_path.exists()
    assert util_path.is_dir()

    repo_path = util_path.parent.absolute()
    assert repo_path.exists()
    assert repo_path.is_dir()
    return repo_path


if "__main__" == __name__:
    main()
