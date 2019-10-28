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
    assert 1 < len(argv)
    ipynb_filename = argv[1]
    assert os.path.exists(ipynb_filename), ipynb_filename

    for k, cell in enumerate(gen.gen_cells(ipynb_filename)):
        if 'code' == cell['cell_type']:
            print(f'In[{k}]')
            print(cell['source'])


def is_line_to_separate(line:str, sep=' % ') -> bool:
    return line.startswith('print') and sep in line


def strip_parentheses(line:str) -> str:
    result = line.strip()

    if '(' == result[0]:
        result = result[1:]

    if ')' == result[-1]:
        result = result[:-1]

    return result


def separate_line(line:str) -> str:
    split = strip_parentheses(line.strip('print')).split(' % ')
    assert 2 == len(split)
    return strip_parentheses(split[-1])


if "__main__" == __name__:
    main(sys.argv)
