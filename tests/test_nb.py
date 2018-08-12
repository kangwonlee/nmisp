# ref : Francesco Mosconi, Travis + Anaconda + Jupyter, https://github.com/ghego/travis_anaconda_jupyter


import os
import pytest
import subprocess
import tempfile


def check_kernel_spec():
    # https://jupyter-client.readthedocs.io/en/latest/api/kernelspec.html
    import jupyter_client.kernelspec as jk

    kernel_spec_manager = jk.KernelSpecManager()

    print(kernel_spec_manager.get_all_specs())


def _exec_notebook(path):
    # http://nbconvert.readthedocs.io/en/latest/execute_api.html
    # ijstokes et al, Command line execution of a jupyter notebook fails in default Anaconda 4.1, https://github.com/Anaconda-Platform/nb_conda_kernels/issues/34
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=1000",
                "--ExecutePreprocessor.kernel_name=python",
                "--output", fout.name, path]
        subprocess.check_call(args)


folder_list = (
    '00_introduction', 
    '01_root_finding', 
    '02_num_int', 
    '03_linear_algebra_1', 
    '04_ode', 
    '05_linear_algebra_2',
)


# https://docs.pytest.org/en/latest/example/parametrize.html
@pytest.mark.parametrize("folder", folder_list)
def test_ipynb_in_folder(folder):
    path = os.path.join(os.pardir, folder)
    ext = 'ipynb'

    # recursive loop
    for root, dirnames, filenames in os.walk(path):
        if 'ipynb_checkpoints' not in root:
            # files loop
            for filename in filenames:
                if os.path.splitext(filename)[-1].endswith(ext):
                    print('test() : %s %s' % (root, filename))
                    _exec_notebook(os.path.join(root, filename))
