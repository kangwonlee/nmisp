"""
Importing sympy example a .py file into a Jupyter notebook file.
Following pattern appears repeatedly:
    print("<sympy cmd> %s" % <sympy md>)

This script aims to convert each of such line into an independent cell.

"""


import os
import sys

import nbformat

sys.path.insert(0, os.path.dirname(__file__))

import end_with_two_returns as gen


def main(argv=sys.argv):
    pass


if "__main__" == __name__:
    main(sys.argv)
