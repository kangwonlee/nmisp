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
def temp_proj_root(tmp_path:pathlib.Path):
    """Create a temporary project root with files and directories."""
    root = tmp_path / "my_project"
    root.mkdir()

    # Chapters and files
    (root / "chapter1").mkdir()
    (root / "chapter1" / "notebook1.ipynb").touch()
    (root / "chapter1" / "file1.txt").write_text("content")

    (root / "chapter2").mkdir()
    (root / "chapter2" / "notebook2.ipynb").touch()
    (root / "chapter2" / "file2.txt").write_text("content")
    (root / "chapter2" / "data.txt").touch()

    # Ignored directory
    (root / "__pycache__").mkdir()
    (root / "__pycache__" / "cache_file.txt").write_text("content") 
    (root / "__pycache__" / "do_not_run.ipynb").write_text("content") 

    return root


def test_os_walk_if_not_ignore__basic(temp_proj_root:pathlib.Path):
    result_dirs = {pathlib.Path(root_name) for root_name, _, _ in rcu.os_walk_if_not_ignore(str(temp_proj_root))}
    expected_dirs = {temp_proj_root, temp_proj_root / "chapter1", temp_proj_root / "chapter2"}
    assert result_dirs == expected_dirs


def test_os_walk_if_not_ignore__ignore(temp_proj_root:pathlib.Path):
    result_dirs = [pathlib.Path(root_name) for root_name, _, _ in rcu.os_walk_if_not_ignore(str(temp_proj_root))]
    assert temp_proj_root / "__pycache__" not in result_dirs


def test_iter_ipynb_default_root(temp_proj_root:pathlib.Path, monkeypatch):
    """Test with the default project root."""
    monkeypatch.setattr(rcu, "get_proj_root", lambda: temp_proj_root)  # Patch get_proj_root
    expected_files = {
        temp_proj_root / "chapter1" / "notebook1.ipynb",
        temp_proj_root / "chapter2" / "notebook2.ipynb",
    }
    result_files = set(
        map(
            pathlib.Path,
            rcu.iter_ipynb(),
        )
    )
    assert result_files == expected_files


def test_iter_ipynb_specific_root(temp_proj_root:pathlib.Path):
    """Test with a specific root directory."""
    chapter2_path = temp_proj_root / "chapter2"
    expected_files = {chapter2_path / "notebook2.ipynb"}
    result_files = set(
        map(
            pathlib.Path,
            rcu.iter_ipynb(str(chapter2_path)),
        )
    )
    assert result_files == expected_files


def test_iter_ipynb_ignores_directories(temp_proj_root:pathlib.Path, monkeypatch):
    """Test that ignored directories are skipped."""
    monkeypatch.setattr(rcu, "get_proj_root", lambda: temp_proj_root)
    result_files = map(
        pathlib.Path,
        rcu.iter_ipynb()
    )  # Use map for efficient conversion
    for file in result_files:
        assert "__pycache__" not in file.parts


if "__main__" == __name__:
    pytest.main([__file__])
