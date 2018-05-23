import os
import shutil
import unittest

import nb_file_util as fu
import ipynb_remove_output as rm


class TestRemoveOutput(unittest.TestCase):
    def setUp(self):
        self.original_file_name =  os.path.join('tests', 'sample_with_output.ipynb') 
        self.del_this_later = os.path.join('tests', 'del_this.ipynb')

        shutil.copy(self.original_file_name, self.del_this_later)

        if os.path.exists(self.del_this_later):
            self.input_file_name = self.del_this_later
        else:
            raise IOError('Unable to create %s' % self.del_this_later)

    def tearDown(self):
        if os.path.exists(self.del_this_later):
            os.remove(self.del_this_later)

    def test_delete_output_file(self):
        # object under test
        rm_cp = rm.CellProcessorDeleteOutput()

        # apply object under test on the input test file
        p = fu.FileProcessor(self.input_file_name, rm_cp)

        p.process_nb_file(b_write_file=True)

        node_dict = p.read_file()

        cells = node_dict.get('cells', [])

        for cell in cells:
            self.assertFalse(cell.get('outputs'))
