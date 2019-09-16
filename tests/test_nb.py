# ref : Francesco Mosconi, Travis + Anaconda + Jupyter, https://github.com/ghego/travis_anaconda_jupyter


import itertools
import os
import subprocess
import tempfile

import pytest


def check_kernel_spec():
    # https://jupyter-client.readthedocs.io/en/latest/api/kernelspec.html
    import jupyter_client.kernelspec as jk

    kernel_spec_manager = jk.KernelSpecManager()

    print(kernel_spec_manager.get_all_specs())


def _exec_notebook_nix(path):
    """
    Run the ipynb file of path
    Raise exception if any error
    """
    # http://nbconvert.readthedocs.io/en/latest/execute_api.html
    # ijstokes et al, Command line execution of a jupyter notebook fails in default Anaconda 4.1, https://github.com/Anaconda-Platform/nb_conda_kernels/issues/34
    # obtain a temporary filename
    # https://docs.python.org/3/library/tempfile.html
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        # prepare a command running .ipynb file while converting
        args = [
            "jupyter", # name of program
            "nbconvert", # option
            "--to", "notebook", # conver to another ipynb file
            "--execute", # run while convering
            "--ExecutePreprocessor.timeout=1000",
            "--ExecutePreprocessor.kernel_name=python",
            "--output", fout.name, # output file name
            path    # input file name
        ]
        # run the command above
        # and raise an exception if error
        subprocess.check_call(args)


def _exec_notebook_win(path):
    """
    Run the ipynb file of path
    Raise exception if any error
    """
    # http://nbconvert.readthedocs.io/en/latest/execute_api.html
    # ijstokes et al, Command line execution of a jupyter notebook fails in default Anaconda 4.1, https://github.com/Anaconda-Platform/nb_conda_kernels/issues/34
    # obtain a temporary filename
    # https://docs.python.org/3/library/tempfile.html
    ftemp = tempfile.NamedTemporaryFile(suffix=".ipynb")
    filename = os.path.join(os.getcwd(), os.path.basename(ftemp.name))
    ftemp.close()

    # prepare a command running .ipynb file while converting
    args = [
        "jupyter", # name of program
        "nbconvert", # option
        "--to", "notebook", # conver to another ipynb file
        "--execute", # run while convering
        "--ExecutePreprocessor.timeout=3600",
        "--ExecutePreprocessor.kernel_name=python",
        "--output", filename, # output file name
        path    # input file name
    ]

    try:
        # run the command above
        # and raise an exception if error
        subprocess.check_call(args)
    except BaseException as e:
        print(e)
        if os.path.exists(filename):
            os.remove(filename)
        raise e

    print('success')
    if os.path.exists(filename):
        os.remove(filename)


# https://docs.pytest.org/en/latest/fixture.html#scope-sharing-a-fixture-instance-across-tests-in-a-class-module-or-session
def get_exec_notebook():
    # https://docs.python.org/3/library/platform.html#cross-platform
    os_to_function_table = {
        'posix': _exec_notebook_nix,
        'nt': _exec_notebook_win,
    }

    return os_to_function_table.get(os.name, _exec_notebook_nix)


def test_is_ignore():

    true_00 = os.sep.join('~/Documents/Python Scripts/proj/subfolder/.ipynb_checkpoints'.split('/'))
    assert is_ignore(true_00)

    false_00 = os.sep.join('~/Documents/Python Scripts/proj/subfolder'.split('/'))
    assert not is_ignore(false_00)


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


def test_is_ignore_env_ignore_folder(env_ignore_folder_2):
    true_00 = os.sep.join('~/Documents/Python Scripts/proj/subfolder/.ipynb_checkpoints'.split('/'))
    assert is_ignore(true_00)

    true_01 = os.sep.join('~/Documents/Python Scripts/proj/subfolder'.split('/'))
    assert is_ignore(true_01)

    false_00 = os.sep.join('~/Documents/Python Scripts/proj/'.split('/'))
    assert not is_ignore(false_00)


def is_ignore(path):
    path_list = path.split(os.sep)

    ignore_list = get_ignore_list()

    return any(map(lambda path_part: path_part in ignore_list, path_list))


def test_get_ignore_list():
    assert all(get_ignore_list())


def get_ignore_list():
    ignore_list = ['.ipynb_checkpoints', '.git', '__pycache__', '.pytest_cache']

    if 'TEST_IPYNB_IGNORE_FOLDER' in os.environ:
        ignore_list += os.environ['TEST_IPYNB_IGNORE_FOLDER'].split(os.pathsep)

    assert all(map(lambda path: isinstance(path, str), ignore_list))

    return ignore_list


def make_file_list(path='', ext='ipynb'):

    path = os.path.abspath(path)

    if not os.path.exists(path):
        path=os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    file_list = []

    # recursive loop
    for root, _, filenames in os.walk(path):
        if not (is_ignore(root)):
            # files loop
            for filename in filenames:
                if os.path.splitext(filename)[-1].endswith(ext):
                    file_path = os.path.join(root, filename)
                    assert isinstance(file_path, str)
                    assert os.path.exists(file_path), f"File Not Found {file_path}"
                    file_list.append(file_path)

    assert file_list, f"\npath = {path}\nget_ignore_list() = {get_ignore_list()}"

    return file_list


def test_make_file_list(env_ignore_folder_2):

    list_under_test = make_file_list()

    assert list_under_test, "List empty"

    for filename in list_under_test:
        assert isinstance(filename, str)
        assert os.path.exists(filename), f"File Not Found {filename}"
        assert not is_ignore(filename), f"Unexpected file {filename}"


def test_make_file_list_env_input(env_ignore_folder_2):
    list_under_test = make_file_list(
        os.path.abspath(
            os.environ.get('TEST_IPYNB_FOLDER', '')
        )
    )

    assert list_under_test, "List empty"

    for filename in make_file_list(os.path.abspath(
                os.environ.get('TEST_IPYNB_FOLDER', '')
            )):
        assert isinstance(filename, str)
        assert os.path.exists(filename), f"File Not Found {filename}"
        assert not is_ignore(filename), f"Unexpected file {filename}"


# https://docs.pytest.org/en/latest/example/parametrize.html
@pytest.mark.parametrize(
    "filename, _exec_notebook",
    itertools.zip_longest(
        make_file_list(
            os.path.abspath(
                os.environ.get('TEST_IPYNB_FOLDER', '')
            )
        ),
        [get_exec_notebook()], fillvalue=get_exec_notebook()
    )
)


def test_ipynb_file(filename, _exec_notebook):
    print('test() : %s' % filename)
    assert os.path.exists(filename), f"File Not Found {filename}"
    _exec_notebook(filename)


if "__main__" == __name__:
    pytest.main()
