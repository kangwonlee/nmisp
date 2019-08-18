import os

import nbformat


def get_cur_dir():
    return os.path.abspath(os.path.basename(__file__))
