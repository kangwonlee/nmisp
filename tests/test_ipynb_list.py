import os
import pathlib
import sys

from typing import Dict

import pytest

file_path = pathlib.Path(__file__).absolute()
test_folder_path = file_path.parent.absolute()

sys.path.insert(0, str(test_folder_path))

import ipynb_list


@pytest.fixture
def ignore_true() -> pathlib.Path:
    return pathlib.Path('~/Documents/Python Scripts/proj/subfolder/.ipynb_checkpoints')


@pytest.fixture
def ignore_true_in_env2() -> pathlib.Path:
    return pathlib.Path('~/Documents/Python Scripts/proj/subfolder/')


@pytest.fixture
def ignore_false_in_env2() -> pathlib.Path:
    return pathlib.Path('~/Documents/Python Scripts/proj/')


@pytest.fixture(scope="function")
def env_ignore_folder_2() -> Dict[str, str]:

    if 'TEST_IPYNB_IGNORE_FOLDER' in os.environ:
        backup_env = os.environ.get('TEST_IPYNB_IGNORE_FOLDER', '')
    else:
        backup_env = False

    os.environ['TEST_IPYNB_IGNORE_FOLDER'] = os.pathsep.join(['subfolder', 'temp'])

    yield os.environ

    # restore env var
    if isinstance(backup_env, os.PathLike):
        os.environ['TEST_IPYNB_IGNORE_FOLDER'] = backup_env
    else:
        del os.environ['TEST_IPYNB_IGNORE_FOLDER']


def test_is_ignore_env_ignore_folder(env_ignore_folder_2, ignore_true, ignore_true_in_env2, ignore_false_in_env2):
    assert ipynb_list.is_ignore(ignore_true)

    assert ipynb_list.is_ignore(ignore_true_in_env2)

    assert not ipynb_list.is_ignore(ignore_false_in_env2)


def test_get_filename_tuple(env_ignore_folder_2):

    tuple_under_test = ipynb_list.get_filename_tuple()

    assert tuple_under_test, "List empty"

    for filename in tuple_under_test:
        assert isinstance(filename, str)
        assert os.path.exists(filename), f"File Not Found {filename}"
        assert not ipynb_list.is_ignore(pathlib.Path(filename)), f"Unexpected file {filename}"


def test_get_ignore_list():
    assert all(ipynb_list.get_ignore_set())


def test_is_ignore__true(ignore_true):
    assert ipynb_list.is_ignore(ignore_true)


def test_is_ignore__false(ignore_true_in_env2):
    assert not ipynb_list.is_ignore(ignore_true_in_env2)


def test_get_filename_tuple__env_input(env_ignore_folder_2):
    list_under_test = ipynb_list.get_filename_tuple(
        os.path.abspath(
            os.environ.get('TEST_IPYNB_FOLDER', '')
        )
    )

    assert list_under_test, "List empty"

    for filename in ipynb_list.get_filename_tuple(os.path.abspath(
                os.environ.get('TEST_IPYNB_FOLDER', '')
            )):
        assert isinstance(filename, str)
        assert os.path.exists(filename), f"File Not Found {filename}"
        assert not ipynb_list.is_ignore(pathlib.Path(filename)), f"Unexpected file {filename}"
