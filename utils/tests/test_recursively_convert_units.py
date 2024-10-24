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


@pytest.fixture
def temp_proj_root(tmp_path):
    """Create a temporary project root with ipynb files."""
    root = tmp_path / "my_project"
    root.mkdir()
    (root / "chapter1").mkdir()
    (root / "chapter2").mkdir()
    (root / "chapter1" / "notebook1.ipynb").touch()
    (root / "chapter2" / "notebook2.ipynb").touch()
    (root / "chapter2" / "data.txt").touch()  # Non-ipynb file
    (root / "__pycache__").mkdir()  # Ignored directory
    return root


def test_iter_ipynb_default_root(temp_proj_root, monkeypatch):
    """Test with the default project root."""
    monkeypatch.setattr(rcu, "get_proj_root", lambda: temp_proj_root)  # Patch get_proj_root
    expected_files = {
        temp_proj_root / "chapter1" / "notebook1.ipynb",
        temp_proj_root / "chapter2" / "notebook2.ipynb",
    }
    result_files = set(rcu.iter_ipynb())
    assert result_files == expected_files


def test_iter_ipynb_specific_root(temp_proj_root):
    """Test with a specific root directory."""
    chapter2_path = temp_proj_root / "chapter2"
    expected_files = {chapter2_path / "notebook2.ipynb"}
    result_files = set(rcu.iter_ipynb(str(chapter2_path)))  # Pass chapter2 as root
    assert result_files == expected_files


def test_iter_ipynb_ignores_directories(temp_proj_root, monkeypatch):
    """Test that ignored directories are skipped."""
    monkeypatch.setattr(rcu, "get_proj_root", lambda: temp_proj_root)
    result_files = list(rcu.iter_ipynb())
    for file in result_files:
        assert "__pycache__" not in file.parts


if "__main__" == __name__:
    pytest.main([__file__])
