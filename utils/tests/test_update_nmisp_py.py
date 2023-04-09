import pathlib
import pytest
import subprocess
import sys

utils_tests_folder_path = pathlib.Path(__file__).parent.absolute()
assert utils_tests_folder_path.exists(), utils_tests_folder_path
assert utils_tests_folder_path.is_dir()

utils_folder_path = utils_tests_folder_path.parent
assert utils_folder_path.is_dir()
assert (utils_folder_path / "update_nmisp_py.py").exists(), utils_folder_path

sys.path.insert(
    0,
    str(utils_folder_path),
)

import update_nmisp_py as unp


@pytest.fixture
def repo_name():
    return "nmisp_py"


@pytest.fixture
def org_name():
    return "kangwonlee"


@pytest.fixture
def cloned_repo(tmp_path, org_name, repo_name):
    subprocess.check_call(
        ["git", "clone", f"https://github.com/{org_name}/{repo_name}"],
        cwd=tmp_path,
    )
    result = tmp_path / repo_name

    assert result.exists(), result
    assert result.is_dir()

    return result


def test_update_nmisp_py_branch_business__slash_not_existing(cloned_repo):
    """
    Test the branch_business function
    """

    new_branch_name = "__new__branch__/__name__"

    # function under test
    unp.branch_business(cloned_repo, new_branch_name)

    # get the name of the branch of the cloned repository
    current_cloned_branch = subprocess.check_output(
        ["git", "branch", "--show-current"],
        cwd=cloned_repo,
        encoding="utf-8",
    ).strip()

    assert current_cloned_branch == new_branch_name


def test_update_nmisp_py_branch_business__slash_existing(cloned_repo):
    """
    Test the branch_business function
    """

    new_branch_name = "_test_branch_/_existing_"

    # function under test
    unp.branch_business(cloned_repo, new_branch_name)

    # get the name of the branch of the cloned repository
    current_cloned_branch = subprocess.check_output(
        ["git", "branch", "--show-current"],
        cwd=cloned_repo,
        encoding="utf-8",
    ).strip()

    assert current_cloned_branch == new_branch_name
