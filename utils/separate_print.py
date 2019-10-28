"""
Importing sympy example a .py file into a Jupyter notebook file.
Following pattern appears repeatedly:
    print("<sympy cmd> %s" % <sympy md>)

This script aims to convert each of such line into an independent cell.

"""


import os
import sys

import nbformat


def main(argv=sys.argv):
    pass


if "__main__" == __name__:
    main(sys.argv)
