# ref : Francesco Mosconi, Travis + Anaconda + Jupyter, https://github.com/ghego/travis_anaconda_jupyter


import os
import subprocess
import tempfile

import pytest


def check_kernel_spec():
    import jupyter_client.kernelspec as jk
    # https://jupyter-client.readthedocs.io/en/latest/api/kernelspec.html

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
    filename = os.path.join(os.getcwd(), os.path.split(ftemp.name)[-1])
    ftemp.close()

    # prepare a command running .ipynb file while converting
    args = [
        "jupyter", # name of program
        "nbconvert", # option
        "--to", "notebook", # conver to another ipynb file
        "--execute", # run while convering
        "--ExecutePreprocessor.timeout=1000",
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


# https://docs.python.org/3/library/platform.html#cross-platform
run_this_dict = {
    'posix': _exec_notebook_nix,
    'nt': _exec_notebook_win,
}


print(f"os.name = {os.name}")
_exec_notebook = run_this_dict.get(os.name, _exec_notebook_nix)


folder_list = (
    os.path.abspath(os.path.join(os.path.split(__file__)[0], os.pardir)),
)


# https://docs.pytest.org/en/latest/example/parametrize.html
@pytest.mark.parametrize("folder", folder_list)
def test_ipynb_in_folder(folder):
    path = os.path.join(os.pardir, folder)
    ext = 'ipynb'

    # recursive loop
    for root, _, filenames in os.walk(path):
        if 'ipynb_checkpoints' not in root:
            # files loop
            for filename in filenames:
                if os.path.splitext(filename)[-1].endswith(ext):
                    print('test() : %s %s' % (root, filename))
                    _exec_notebook(os.path.join(root, filename))
