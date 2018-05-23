import os
import unittest

import nb_file_util as fu
import ipynb_remove_output as rm


class TestRemoveOutput(unittest.TestCase):
    def setUp(self):
        self.input_file_name =  os.path.join('tests', 'sample_with_output.ipynb') 

    def test_delete_output_file(self):
        rm_cp = rm.CellProcessorDeleteOutput()
        p = fu.FileProcessor(self.input_file_name, rm_cp)

        p.process_nb_file(b_write_file=True)

        node_dict = p.read_file()

        cells = node_dict.get('cells', [])

        for k, cell in enumerate(cells):
            self.assertFalse(cell.get('outputs'))
