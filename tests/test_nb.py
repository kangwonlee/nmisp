# ref : Francesco Mosconi, Travis + Anaconda + Jupyter, https://github.com/ghego/travis_anaconda_jupyter
import os
import pathlib
import subprocess
import sys

import pytest

file_path = pathlib.Path(__file__).absolute()
test_folder_path = file_path.parent.absolute()

sys.path.insert(0, str(test_folder_path))

import ipynb_list


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


# https://docs.pytest.org/en/latest/example/parametrize.html
@pytest.mark.parametrize(
    "filename", ipynb_list.get_filename_tuple(
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
    pytest.main(['-n', 'auto', __file__])
