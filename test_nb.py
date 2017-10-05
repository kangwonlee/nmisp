# ref : Francesco Mosconi, Travis + Anaconda + Jupyter, https://github.com/ghego/travis_anaconda_jupyter


import os
import subprocess
import tempfile


def _exec_notebook(path):
    # http://nbconvert.readthedocs.io/en/latest/execute_api.html
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=1000",
                "--ExecutePreprocessor.kernel_name=python3",
                "--output", fout.name, path]
        subprocess.check_call(args)


def test():
    path = os.pardir
    ext = 'ipynb'

    # recursive loop
    for root, dirnames, filenames in os.walk(path):
        if 'ipynb_checkpoints' not in root:
            # files loop
            for filename in filenames:
                if os.path.splitext(filename)[-1].endswith(ext):
                    print('test() : %s %s' % (root, filename))
                    _exec_notebook(os.path.join(root, filename))
