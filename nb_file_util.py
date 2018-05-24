import os
import subprocess

import nbformat


class FileProcessor(object):
    """
    Interface to jupyter notebook file
    """

    def __init__(self, nb_filename, cell_processor=None):
        self.nb_filename = nb_filename
        self.nb_node = None
        if cell_processor is None:
            cell_processor = CellProcessorBase()
        self.cell_list_processor = CellListProcessor(cell_processor=cell_processor)

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

    def process_nb_file(self, nb_filename=None, b_write_file=False):
        # TODO : see if use_default_filename_if_missing() is necessary here;
        #        read_file() calls it too
        nb_filename = self.use_default_filename_if_missing(nb_filename)

        # read the content of the file
        self.nb_node = self.read_file(nb_filename)

        # keys : values
        # 'cells' : contents of the notebook file
        # 'metadata' : python version, ipython version
        # 'nbformat', 'nbformat_minor' : ipython notebook version

        result = {'file name': nb_filename, 'result': self.process_nb_node()}

        if b_write_file:
            self.write_file(nb_filename)

        return result

    def process_nb_node(self):
        if self.nb_node is None:
            self.read_file()

        result = None

        if 'cells' in self.nb_node:

            self.cell_list_processor.set_cell_list(self.nb_node['cells'])
            result = self.cell_list_processor.process_cells()
        else:
            raise ValueError("nb node does not have 'cells'")

        return result


class CellListProcessor(object):
    def __init__(self, cell_list=None, cell_processor=None):
        self.cell_list = cell_list
        if cell_processor is None:
            cell_processor = CellProcessorBase()
        self.cp = cell_processor

    def set_cell_list(self, cell_list):
        self.cell_list = cell_list

    def remove_outputs(self):
        cp = CellProcessorBase()
        for cell in self.cell_list:
            cp.set_cell(cell)
            cp.remove_cell_output()

    def process_cells(self):
        result = []

        for cell_number, cell in enumerate(self.cell_list):
            self.cp.set_cell(cell)
            cell_result = self.cp.process_cell()
            if cell_result:
                result.append({'cell number': cell_number, 'result': cell_result})

        return result


class CellProcessorBase(object):
    def __init__(self, cell=None):
        """

        :param dict cell:
        """
        self.cell = cell

    def set_cell(self, cell):
        """

        :param dict cell:
        :return:
        """
        self.cell = cell

    def is_code(self):
        """

        :return:
        """
        return 'code' == self.cell['cell_type']

    def has_field(self, field):
        """

        :param str field:
        :return:
        """
        return field in self.cell

    def has_output(self):
        return self.has_field('outputs')

    def has_source(self):
        return self.has_field('source')

    def remove_cell_output(self):
        if self.is_code():
            self.cell['outputs'] = []
            self.cell['execution_count'] = None

    def process_cell(self):
        # virtual method
        raise NotImplementedError()
