import functools
import itertools
import multiprocessing as mp
import pathlib
import subprocess

import nbformat
from nbformat.v4.nbbase import new_code_cell

class FileProcessor(object):
    """
    Interface to jupyter notebook file
    """

    def __init__(self, nb_filename, cell_processor=None):
        self.nb_filename = pathlib.Path(nb_filename)
        self.nb_node = None
        if cell_processor is None:
            cell_processor = CellProcessorBase()
        self.cell_list_processor = CellListProcessor(cell_processor=cell_processor)

    def read_file(self, nb_filename=None):
        nb_filename = self.use_default_filename_if_missing(nb_filename)
        assert nb_filename.exists(), nb_filename

        return nbformat.reads(
            nb_filename.read_text(),
            nbformat.NO_CONVERT
        )

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


@functools.lru_cache(maxsize=1)
def get_upper_folder() -> pathlib.Path:
    proj_folder = pathlib.Path(__file__).parent.parent.absolute()
    assert proj_folder.is_dir(), proj_folder
    assert (proj_folder / ".gitignore").exists(), proj_folder
    return proj_folder


def one_level_ipynb(proj_path:pathlib.Path=get_upper_folder()) -> pathlib.Path:
    """
    generator of full paths to ipynb files one level under the given folder
    """
    proj_path = pathlib.Path(proj_path).absolute()
    assert proj_path.is_dir(), proj_path

    for item in proj_path.iterdir():
        if item.is_dir() and (not item.name.startswith('.')):
            chapter_dir = item.absolute()
            for chapter_item in chapter_dir.iterdir():
                if chapter_item.is_file() and ("ipynb" == chapter_item.suffix.lower()):
                    yield chapter_item


def read_nodes_from_ipynb(full_path_ipynb:str) -> nbformat.NotebookNode:
    full_path_ipynb = pathlib.Path(full_path_ipynb).absolute()
    assert full_path_ipynb.exists(), full_path_ipynb

    with full_path_ipynb.open('rb') as nb_file:
        nb_node = nbformat.read(nb_file, nbformat.NO_CONVERT)

    return nb_node


def write_nodes_to_ipynb(full_path_ipynb:str, nb_node:nbformat.NotebookNode):
    nbformat.write(nb_node, full_path_ipynb)


def insert_code_cell(nb_node:nbformat.NotebookNode, index:int, code:str) -> nbformat.NotebookNode:
    new_cell = nbformat.v4.new_code_cell(source=code)

    if "id" in new_cell:
        del new_cell["id"]

    nb_node["cells"].insert(index, new_cell)

    return nb_node


def insert_code_cell_to_ipynb(index:int, code:str, full_path_ipynb:str, b_allow_duplicate:bool=False):
    nb_node = read_nodes_from_ipynb(full_path_ipynb)
    if b_allow_duplicate or (nb_node["cells"][index]["source"] != code):
        insert_code_cell(nb_node, index, code)
        write_nodes_to_ipynb(full_path_ipynb, nb_node)


def add_code_to_all_ipynb_tree(index:int, code:str, path:str=get_upper_folder(), b_debug:bool=False):
    def gen_i_c_p():
        for full_path in one_level_ipynb(path):
            yield index, code, full_path
    if b_debug:
        list(itertools.starmap(insert_code_cell_to_ipynb, gen_i_c_p()))
    else:
        pool = mp.Pool(mp.cpu_count()-1)
        pool.starmap(insert_code_cell_to_ipynb, gen_i_c_p())
        pool.close()
        pool.join()


def remove_cell_id_from_nodes(nb_node:nbformat.NotebookNode) -> None:
    """
    Sometimes, ipynb files may contain cell IDs
    Also, sometimes, some users may prefer metadata without IDs

    =======
    Example
    =======
    >>> ipynb_full_path = "sample.ipynb"
    >>> nodes = read_nodes_from_ipynb(ipynb_full_path)
    >>> remove_cell_id_from_nodes(nodes)
    >>> write_nodes_to_ipynb(full_path, nodes)
    """

    for cell in nb_node["cells"]:
        if "id" in cell["metadata"]:
            del cell["metadata"]["id"]
