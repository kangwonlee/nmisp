# ref : Francesco Mosconi, Travis + Anaconda + Jupyter, https://github.com/ghego/travis_anaconda_jupyter

import os
import pathlib
import subprocess

from typing import Set, Tuple

import pytest


def _exec_notebook(path, tmp_path):
    """
    Run the ipynb file of path
    Raise exception if any error
    """
    # http://nbconvert.readthedocs.io/en/latest/execute_api.html
    # ijstokes et al, Command line execution of a jupyter notebook fails in default Anaconda 4.1, https://github.com/Anaconda-Platform/nb_conda_kernels/issues/34
    # obtain a temporary filename
    # https://docs.python.org/3/library/tempfile.html
    # https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html

    tmp_ipynb = (tmp_path / pathlib.Path(path).name).absolute()
    args = (
        "jupyter", # name of program
        "nbconvert", # option
        "--to", "notebook", # conver to another ipynb file
        "--execute", # run while convering
        "--ExecutePreprocessor.timeout=1000",
        "--ExecutePreprocessor.kernel_name=python",
        "--output", str(tmp_ipynb), # output file name
        path    # input file name
    )
    # run the command above
    # and raise an exception if error
    subprocess.check_call(args, cwd=path.parent.absolute())


@pytest.fixture
def ignore_true() -> pathlib.Path:
    return pathlib.Path('~/Documents/Python Scripts/proj/subfolder/.ipynb_checkpoints')


@pytest.fixture
def ignore_true_in_env2() -> pathlib.Path:
    return pathlib.Path('~/Documents/Python Scripts/proj/subfolder/')


@pytest.fixture
def ignore_false_in_env2() -> pathlib.Path:
    return pathlib.Path('~/Documents/Python Scripts/proj/')


def test_is_ignore__true(ignore_true):
    assert is_ignore(ignore_true)


def test_is_ignore__false(ignore_true_in_env2):
    assert not is_ignore(ignore_true_in_env2)


@pytest.fixture(scope="function")
def env_ignore_folder_2():

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
    assert is_ignore(ignore_true)

    assert is_ignore(ignore_true_in_env2)

    assert not is_ignore(ignore_false_in_env2)


def is_ignore(path:pathlib.Path) -> bool:
    return (set(path.parts).intersection(get_ignore_set()))


def test_get_ignore_list():
    assert all(get_ignore_set())


def get_ignore_set() -> Set[str]:
    ignore_list = ['.ipynb_checkpoints', '.git', '__pycache__', '.pytest_cache']

    if 'TEST_IPYNB_IGNORE_FOLDER' in os.environ:
        ignore_list += os.environ['TEST_IPYNB_IGNORE_FOLDER'].split(os.pathsep)

    assert all(map(lambda path: isinstance(path, str), ignore_list))

    return set(ignore_list)


def get_filename_tuple(path='', ext='ipynb') -> Tuple[str]:

    path = pathlib.Path(path).absolute()

    if not path.exists():
        print(f"{path} does not exist.", end=' ')
        path = pathlib.Path(__file__).parent.parent.absolute()
        print(f"Using {path}.")

    return tuple(
        map(
            str,    # pytest param needs str for function name
            filter(
                lambda f_path: not is_ignore(f_path.parent.relative_to(path)),
                path.glob(f'**/*.{ext}')
            )        
        )
    )


def test_get_filename_tuple(env_ignore_folder_2):

    tuple_under_test = get_filename_tuple()

    assert tuple_under_test, "List empty"

    for filename in tuple_under_test:
        assert isinstance(filename, str)
        assert os.path.exists(filename), f"File Not Found {filename}"
        assert not is_ignore(pathlib.Path(filename)), f"Unexpected file {filename}"


def test_get_filename_tuple__env_input(env_ignore_folder_2):
    list_under_test = get_filename_tuple(
        os.path.abspath(
            os.environ.get('TEST_IPYNB_FOLDER', '')
        )
    )

    assert list_under_test, "List empty"

    for filename in get_filename_tuple(os.path.abspath(
                os.environ.get('TEST_IPYNB_FOLDER', '')
            )):
        assert isinstance(filename, str)
        assert os.path.exists(filename), f"File Not Found {filename}"
        assert not is_ignore(pathlib.Path(filename)), f"Unexpected file {filename}"


# https://docs.pytest.org/en/latest/example/parametrize.html
@pytest.mark.parametrize(
    "filename", get_filename_tuple(
        os.path.abspath(
            os.environ.get('TEST_IPYNB_FOLDER', '')
        )
    ),
)


def test_ipynb_file(filename, tmp_path):
    print('test() : %s' % filename)
    assert os.path.exists(filename), f"File Not Found {filename}"
    _exec_notebook(pathlib.Path(filename), tmp_path)


if "__main__" == __name__:
    pytest.main()
