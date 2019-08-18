import os

import nbformat


def get_cur_dir():
    return os.path.abspath(os.path.basename(__file__))


def get_par_dir():
    return os.path.abspath(os.path.join(os.path.basename(__file__), os.pardir))
