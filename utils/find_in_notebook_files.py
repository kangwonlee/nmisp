"""
Find (and possibly Replace) in Notebook Files


1. Commandline arguments
$ python find_in_notebook_files.py replace_this to_this b_replace b_verbose b_arm

replace_this : Find this string
to_this : Replace to this string
b_replace : Replace if true
b_verbose : Show all cases
b_arm : If true, overwrite


2. Config file
If not all arguments available, this program would try to use "finf.cfg" file

--------------------
Sample finf.cfg file
--------------------
[control]
verbose = True
replace = True
arm = False

[string]
replace this = r'#+\s+(하중)$'
to this = '''하중<br>Load'''
--------------------
[string] section can be regular expressions
"""


import ast
import configparser as configparser
import json
import os
import pathlib
import re
import sys

from typing import Any, Dict, Tuple

import nbformat

import recursively_convert_units as rcu


CELL = Dict[str, Any]


class NotebookFile:
    allowed_id:Tuple[str]=("view-in-github",)
    allowed_colab:Tuple[str]=tuple()

    # constructor
    def __init__(self, ipynb_full_path):
        self.ipynb_full_path = ipynb_full_path
        self.nb_node = nbformat.read(ipynb_full_path, nbformat.NO_CONVERT)

    def gen_cells(self):
        """Iterate over cells in the notebook."""
        for cell in self.nb_node.cells:
            yield cell

    def overwrite_cell(self, index:int, cell:dict):
        """Overwrite a cell at a specific index."""
        new_cell = nbformat.NotebookNode(cell)
        self.nb_node.cells[index] = new_cell

    def insert_cell(self, index:int, cell:dict):
        """Insert a new cell at a specific index."""
        new_cell = nbformat.NotebookNode(cell)
        self.nb_node.cells.insert(index, new_cell)

    def validate(self):
        return nbformat.validate(self.nb_node)

    def split_source_lines(self):
        """Split cell source code into individual lines."""
        for cell in self.gen_cells():
            if "source" in cell and isinstance(cell.source, str):
                cell.source = [line+'\n' for line in cell.source.splitlines()]

    def write(self, new_file_full_path):
        output_path = pathlib.Path(new_file_full_path)

        self.split_source_lines()

        with output_path.open('w', encoding='utf-8') as f:
            json.dump(self.nb_node, f, indent=1, ensure_ascii=False)

    def remove_cell_id_from_nodes(self) -> bool:
        """Remove cell IDs except for those in the allowed list."""
        b_write_list = []

        for cell in self.gen_cells():
            b_write_list.append(self.remove_id_from_a_cell(cell))
            b_write_list.append(self.remove_colab_from_a_cell(cell))

        return any(b_write_list)

    def remove_colab_from_a_cell(self, cell:CELL) -> bool:
        """Remove colab from a single code cell."""
        b_write = False
        if "metadata" in cell:
            if "colab" in cell["metadata"]:
                if cell["metadata"]["colab"] not in self.allowed_colab:
                    del cell["metadata"]["colab"]
                    b_write = True
        if "colab" in cell:
            del cell["colab"]
            b_write = True

        return (b_write)

    def remove_id_from_a_cell(self, cell:CELL) -> bool:
        """Remove cell IDs from a single code cell."""
        b_write = False
        if "metadata" in cell:
            if "id" in cell["metadata"]:
                if cell["metadata"]["id"] not in self.allowed_id:
                    del cell["metadata"]["id"]
                    b_write = True
        if "id" in cell:
            del cell["id"]
            b_write = True

        return (b_write)

    def remove_blank_spaces_from_nodes(self) -> bool:
        """Remove cell IDs except for those in the allowed list."""
        b_modified_list = []

        for cell in self.gen_cells():
            b_modified_list.append(
                self.remove_blank_spaces_from_a_cell(cell)
            )

        return any(b_modified_list)

    def remove_blank_spaces_from_a_cell(self, cell:CELL) -> bool:
        """Remove trailing whitespace from a single code cell."""
        b_modified = False
        source_str = cell.get("source", '')

        if isinstance(source_str, list):
            source_str = ''.join(source_str)
        elif not isinstance(source_str, str):
            raise TypeError(f'"source" is not a str : {type(source_str)}')

        if source_str:
            source_lines = source_str.splitlines()
            new_source_lines = [line.rstrip() for line in source_lines]

            new_source_str = '\n'.join(new_source_lines) + '\n'

            if source_str != new_source_str:
                cell["source"] = new_source_str
                b_modified = True

        return (b_modified)

    def assert_no_ids(self):
        """Assert that no cells have IDs except for allowed ones."""
        for c in self.gen_cells():
            assert "id" not in c, c
            if "id" in c.get("metadata"):
                assert c["metadata"]["id"] in self.allowed_id, c


class FindOrReplaceNotebookFile(NotebookFile):
    def __init__(self, ipynb_full_path, replace_this, to_this, b_verbose=False, b_replace=False, b_arm=False):
        """
        If not b_verbose : does not present results
        If not b_replace : search only
        If not b_arm : display only
        If b_arm : rewrite the file
        """
        super().__init__(ipynb_full_path)

        # Find or replace        
        self.replace_this = replace_this
        self.to_this = to_this

        # Operation switches
        self.b_verbose = b_verbose
        self.b_replace = b_replace
        self.b_arm = b_arm
        # To indicate search result
        self.count = 0

    def for_all_cells_in_file_find_or_replace(self):
        """
        For all cells in the notebook file, replace_this -> to_this
        """
        # To initialize the counter everytime a search starts
        self.count = 0

        # Cell loop
        for cell in self.gen_cells():
            self.count = self.find_or_replace_in_one_cell(cell)

        return self.count

    def found(self, cell_dict):
        """
        See if this cell is of interest
        cell_dict : one of the dicts in nb_node.cells
        """
        return (self.replace_this in cell_dict.get('source')) and (self.to_this not in cell_dict.get('source'))

    def find_or_replace_in_one_cell(self, cell):
        """
        Within one cell of the notebook file, replace_this -> to_this
        If not b_verbose : does not present results
        If not b_replace : search only
        """

        # Found
        if self.found(cell):
            # to indicate search result
            self.count += 1

            if self.b_verbose:
                print(self.ipynb_full_path)

                if self.b_replace:
                    marker = 'before'
                else:
                    marker = 'found'

                # Separate found case
                print(('%s ' % marker).ljust(60, '-'))
                print(cell)
                if self.b_replace:
                    # Replacing here
                    self.update_found_cell_dict(cell)
                    print('after '.ljust(60, '-'))
                    print(cell)

                # Separate file
                print('=' * 80)

        return self.count

    def update_found_cell_dict(self, cell_dict):
        """
        Update the cell of interest
        """
        cell_dict['source'] = cell_dict.get('source').replace(self.replace_this, self.to_this)

    def write(self, ipynb_full_path):
        """
        Write if (b_replace and b_verbose and b_arm)
        If same filename but no replacement count, do not overwrite
        """
        if self.b_replace and self.b_verbose and self.b_arm:
            if (
                (ipynb_full_path != self.ipynb_full_path) 
                or (0 < self.count)
               ):
               # If same filename but no replacement count, do not overwrite
                super().write(ipynb_full_path)


class FindOrReplaceNotebookFileRegex(FindOrReplaceNotebookFile):
    def __init__(self, ipynb_full_path, replace_this, to_this, b_verbose=False, b_replace=False, b_arm=False):
        super().__init__(ipynb_full_path, replace_this, to_this, b_verbose, b_replace, b_arm)

        self.replace_this_re = re.compile(replace_this)

    def __del__(self):
        del self.replace_this_re

        super().__del__()

    def found(self, cell_dict):
        return self.replace_this_re.findall(cell_dict.get('source'))

    def update_found_cell_dict(self, cell_dict):
        new_source = self.replace_this_re.sub(self.to_this, cell_dict.get('source'))
        cell_dict['source'] = new_source


def main(argv):

    replace_this, to_this, b_replace, b_verbose, b_arm = get_param(argv)

    if b_verbose:
        if b_replace:
            print('Will try to replace %r to %r' % (replace_this, to_this))
        else:
            print('Will try to find %r' % replace_this)

    count_files = 0
    count_found = 0

    # Chapter loop + file loop
    for chapter_path, ipynb_filename in rcu.gen_ipynb(get_chapter_par_dir()):
        count_files += 1
        count_found += process_one_ipynb(chapter_path, ipynb_filename, replace_this, to_this, b_replace, b_verbose=b_verbose, b_arm=b_arm)

    print('Found %d/%d cases' % (count_found, count_files))


def get_param(argv, default_filename='finf.cfg'):
    """
    Get parameters from commandline argument or default file
    """

    # If commandline argument
    if 5 <= len(argv):
        replace_this, to_this, b_replace, b_verbose, b_arm = argv[0], argv[1], argv[2], argv[3], argv[4]
    # If commandline argument missing
    else:
        config = configparser.ConfigParser()

        if not os.path.exists(default_filename):
            raise IOError('Unable to find {filename} from {cwd}'.format(filename=default_filename, cwd=os.getcwd()))

        config.read(default_filename)

        # to enable more precise control, adopts ast.litearl_eval
        try:
            replace_this = ast.literal_eval(config['string']['replace this'])
            to_this = ast.literal_eval(config['string']['to this'])
        except KeyError as e:
            print("%r\nconfig has sections : %r" % ('string', config.sections()))
            print('config = %r' % config)
            raise e

        # control parameters
        b_verbose = ('True' == config['control']['verbose'])
        b_arm = ('True' == config['control']['arm'])
        b_replace = ('True' == config['control']['replace'])

    return replace_this, to_this, b_replace, b_verbose, b_arm


# Please commit as `b_verbose=False, b_arm=False` for safety
def process_one_ipynb(chapter_path, ipynb_filename, replace_this, to_this, b_replace, b_verbose=False, b_arm=False):
    """
    When ready to use, first set b_verbose to True and evaluate the result even if you are confident
    After a sufficient review, if you still feel confident, if possible commit your files before applying changes
    As you now have a measure to undo the changes, set b_arm to True and run. I hope you best of luck.
    """
    # Full path to the ipynb file to reuse later
    ipynb_full_path = os.path.join(chapter_path, ipynb_filename)

    nb = FindOrReplaceNotebookFileRegex(ipynb_full_path, replace_this, to_this, b_verbose=b_verbose, b_replace=b_replace, b_arm=b_arm)

    # Count number of found items to indicate search result
    count = nb.for_all_cells_in_file_find_or_replace()

    # overwrite
    nb.write(ipynb_full_path)

    return count


def get_chapter_par_dir():
    """
    Absolute path to the parent directory of chapter folders
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


if __name__ == '__main__':
    main(sys.argv[1:])
