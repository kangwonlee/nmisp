"""
Importing sympy example a .py file into a Jupyter notebook file.
Following pattern appears repeatedly:
    print("<sympy cmd> %s" % <sympy md>)

This script aims to convert each of such line into an independent cell.
"""


import os
import sys
import typing

import nbformat

sys.path.insert(0, os.path.dirname(__file__))

import end_with_two_returns as gen


CODE_CELL = nbformat.notebooknode.NotebookNode


def main(argv=sys.argv):
    assert 1 < len(argv)
    ipynb_filename = argv[1]
    assert os.path.exists(ipynb_filename), ipynb_filename

    for k, cell in enumerate(gen.gen_cells(ipynb_filename)):
        if 'code' == cell['cell_type']:
            print(f'# In[{k}]')
            print(cell['source'])


def process_cell(cell:CODE_CELL) -> typing.List[CODE_CELL]:

    result = []

    if 'code' != cell['cell_type']:
        result.append(cell)
    else:
        new_source_list = []
        for line in cell['source'].splitlines():
            if is_line_to_separate(line):
                flush_source_lines(new_source_list, result)
                new_source_list = [separate_line(line)]
            else:
                new_source_list.append(line)

    flush_source_lines(new_source_list, result)

    return result


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
    return split[-1]


def flush_source_lines(new_source_list:typing.List[str], result:typing.List[CODE_CELL]) -> None:
    if new_source_list:
        result.append(get_new_code_cell(new_source_list))


def get_new_code_cell(new_source_list:typing.List[str]) -> CODE_CELL:
    return nbformat.v4.new_code_cell(source='\n'.join(new_source_list))


if "__main__" == __name__:
    main(sys.argv)
