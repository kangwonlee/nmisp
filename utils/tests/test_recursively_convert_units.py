import pathlib
import pytest
import sys


sys.path.insert(
    0,
    str(pathlib.Path(__file__).parent.parent.absolute()),
)


import recursively_convert_units as rcu


@pytest.fixture
def utils_test_folder() -> pathlib.Path:
    return pathlib.Path(__file__).parent.absolute()


@pytest.fixture
def utils_folder(utils_test_folder:pathlib.Path) -> pathlib.Path:
    return utils_test_folder.parent.absolute()


@pytest.fixture
def proj_folder(utils_folder:pathlib.Path) -> pathlib.Path:
    return utils_folder.parent.absolute()


def test__recursively_convert_units__is_ignore__true(utils_test_folder):
    sample_path = utils_test_folder / "sample.ipynb"
    assert rcu.is_ignore(sample_path)


def test__recursively_convert_units__is_ignore__false(proj_folder):
    sample_path = proj_folder / "10_root_finding" / "10_sequential"
    assert not rcu.is_ignore(sample_path)


@pytest.fixture
def temp_dir(tmp_path):  # Use tmp_path instead of tmpdir
    """Create a temporary directory structure for testing."""
    temp_root = tmp_path / "my_project" 
    temp_root.mkdir()
    (temp_root / "chapter1").mkdir()
    (temp_root / "chapter2").mkdir()
    (temp_root / "__pycache__").mkdir()
    (temp_root / "chapter1" / "file1.txt").write_text("content")
    (temp_root / "chapter2" / "file2.txt").write_text("content")
    (temp_root / "__pycache__" / "cache_file.txt").write_text("content")
    return temp_root  # Return the path as a pathlib.Path object

def test_os_walk_if_not_ignore__basic(temp_dir):
    result_dirs = {pathlib.Path(root_name) for root_name, _, _ in rcu.os_walk_if_not_ignore(str(temp_dir))}
    expected_dirs = {temp_dir, temp_dir / "chapter1", temp_dir / "chapter2"}
    assert result_dirs == expected_dirs


def test_os_walk_if_not_ignore__ignore(temp_dir):
    result_dirs = [pathlib.Path(root_name) for root_name, _, _ in rcu.os_walk_if_not_ignore(str(temp_dir))]
    assert temp_dir / "__pycache__" not in result_dirs


if "__main__" == __name__:
    pytest.main([__file__])
