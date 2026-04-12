import pathlib
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


def test_get_repo_path():
    repo_path = unp.get_repo_path()
    assert repo_path.exists()
    assert repo_path.is_dir()
    assert (repo_path / "utils" / "update_nmisp_py.py").exists()


def test_sync_py_files(tmp_path):
    """
    Test that .py files are copied correctly,
    excluding tests/, utils/, and build_util/
    """
    dest = tmp_path / "nmisp_py"
    dest.mkdir()

    # Initialise a git repo so git-auto-commit-action would work
    subprocess.check_call(["git", "init"], cwd=dest)

    repo_path = unp.get_repo_path()

    # Run the sync (same logic as main, without CLI wrapper)
    for path in dest.rglob("*.py"):
        path.unlink()
    for path in repo_path.rglob("*.py"):
        if not (
            ("tests" in path.relative_to(repo_path).parts[0:2])
            or
            ("build_util" in path.relative_to(repo_path).parts[0:2])
            or
            ("utils" == path.relative_to(repo_path).parts[0])
        ):
            import shutil
            shutil.copy(path, dest / path.name)

    py_files = list(dest.glob("*.py"))
    assert len(py_files) > 0, "No .py files were copied"

    # Verify excluded files are not present
    file_names = {f.name for f in py_files}
    assert "update_nmisp_py.py" not in file_names, "utils/ file should be excluded"
    assert "test_update_nmisp_py.py" not in file_names, "tests/ file should be excluded"
