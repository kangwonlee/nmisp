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
