# ref : Francesco Mosconi, Travis + Anaconda + Jupyter, https://github.com/ghego/travis_anaconda_jupyter

import os
import subprocess
import tempfile

import pytest

from . import get_cpp_from_ipynb as gcpp


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


base_path = os.path.abspath(os.path.join(os.path.split(__file__)[0], os.pardir))

folder_list = (
    '.',
)


# https://docs.pytest.org/en/latest/example/parametrize.html
@pytest.mark.parametrize("folder", folder_list)
def test_ipynb_in_folder(folder):
    path = os.path.join(base_path, folder)
    ext = 'ipynb'

    # recursive loop
    for root, _, filenames in os.walk(path):
        if 'ipynb_checkpoints' not in root:
            # files loop
            for filename in filenames:
                if os.path.splitext(filename)[-1].endswith(ext):
                    print('test() : %s %s' % (root, filename))
                    _exec_notebook(os.path.join(root, filename))


# https://docs.pytest.org/en/latest/example/parametrize.html
@pytest.mark.parametrize("folder", folder_list)
def test_cpp_in_ipynb_in_folder(folder):
    path = os.path.join(base_path, folder)
    ext = 'ipynb'

    if gcpp.has_gpp():
        # recursive loop
        # TODO : Consider changing dirnames to '_'
        for root, _, filenames in os.walk(path):
            if 'ipynb_checkpoints' not in root:
                # files loop
                for filename in filenames:
                    if os.path.splitext(filename)[-1].endswith(ext):
                        print('test() : %s %s' % (root, filename))
                        assert gcpp.get_cpp_src_from_ipynb(os.path.join(root, filename))
