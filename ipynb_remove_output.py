"""
Jupyter notebook could be good for educational purpose.
Before release in class, output generated during testing and execution number need to be removed.
"""

import os
import subprocess
import sys

import nbformat


# Use this module to read or write notebook files as particular nbformat versions.

class FileProcessor(object):
    """
    Interface to jupyter notebook file
    """

    def __init__(self, nb_filename):
        self.nb_filename = nb_filename
        self.nb_node = self.read_file()

    def read_file(self, nb_filename=None):
        nb_filename = self.use_default_filename_if_missing(nb_filename)
        assert os.path.exists(nb_filename)

        with open(nb_filename, 'rb') as nb_file:
            txt = nb_file.read()

        nb_node = nbformat.reads(txt.decode(), nbformat.NO_CONVERT)

        return nb_node

    def use_default_filename_if_missing(self, nb_filename):
        if nb_filename is None:
            nb_filename = self.nb_filename
        return nb_filename

    def write_file(self, nb_filename=None):
        nb_filename = self.use_default_filename_if_missing(nb_filename)
        nbformat.write(self.nb_node, nb_filename)

    def execute(self, nb_filename=None):
        nb_filename = self.use_default_filename_if_missing(nb_filename)
        # http://nbconvert.readthedocs.io/en/latest/execute_api.html
        # ijstokes et al, Command line execution of a jupyter notebook fails in default Anaconda 4.1, https://github.com/Anaconda-Platform/nb_conda_kernels/issues/34
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=1000",
                "--ExecutePreprocessor.kernel_name=python", nb_filename]
        subprocess.check_call(args)


def read_file(nb_filename):
    assert os.path.exists(nb_filename)

    txt = ''

    with open(nb_filename, 'rb') as nb_file:
        txt = nb_file.read()

    nb_node = nbformat.reads(txt.decode(), nbformat.NO_CONVERT)

    return nb_node


def process_nb_node(nb_node):
    for cell in nb_node['cells']:
        remove_cell_output(cell)

    return nb_node


def has_symbol(cell):
    """
     if symbol definition line included, return the line numbers and the contents in a list

    :param nbformat.notebooknode.NotebookNode cell:
    :return: list of tuple([line_number, line_content])
    """
    result = []
    if 'code' == cell['cell_type']:
        if 'source' in cell:
            for k, source_line in enumerate(cell['source'].splitlines()):
                if ('sy.symbols' in source_line) or ('sy.Symbol' in source_line):
                    result.append((k, source_line))

    return result


def symbol_lines_in_file(input_file_name):
    file = read_file(input_file_name)
    assert 'cells' in file

    result = []

    cells = file['cells']
    for k, cell in enumerate(cells):
        cell_result = has_symbol(cell)
        if cell_result:
            result.append((k, cell_result))

    return result


def remove_cell_output(cell):
    if 'code' == cell['cell_type']:
        if 'outputs' in cell:
            cell['outputs'] = []
        if 'execution_count' in cell:
            cell['execution_count'] = None


def write_file(nb_node, nb_filename):
    nbformat.write(nb_node, nb_filename)


def process_nb_file(nb_filename):
    nb_node = read_file(nb_filename)

    processed_node = process_nb_node(nb_node)

    write_file(processed_node, nb_filename)


if __name__ == '__main__':

    def main(argv):
        if 1 < len(argv):
            filename = argv[1]
            process_nb_file(filename)
        else:
            print("Usage : python %s <notebook file path>" % os.path.split(__file__)[-1])
            help(nbformat)


    main(sys.argv)
