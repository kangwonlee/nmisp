import subprocess
import tempfile
import unittest

import ipynb_remove_output as nbutils

null = dir(nbutils)


class TestNButils(unittest.TestCase):
    def test_sample_ipynb(self):
        # should run without an exception
        _exec_notebook('sample.ipynb')


def _exec_notebook(path):
    # http://nbconvert.readthedocs.io/en/latest/execute_api.html
    # ijstokes et al, Command line execution of a jupyter notebook fails in default Anaconda 4.1, https://github.com/Anaconda-Platform/nb_conda_kernels/issues/34
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=1000",
                "--ExecutePreprocessor.kernel_name=python", path]
        subprocess.check_call(args)


if __name__ == '__main__':
    unittest.main()
    # finished running
