import pathlib
import shutil
import unittest

import nb_file_util as fu
import ipynb_remove_output as rm

utils_tests_folder_path = pathlib.Path(__file__).parent.absolute()
assert utils_tests_folder_path.exists(), utils_tests_folder_path
assert utils_tests_folder_path.is_dir()


class TestRemoveOutput(unittest.TestCase):
    def setUp(self):
        self.original_file_name = utils_tests_folder_path / 'sample_with_output.ipynb'
        assert self.original_file_name.exists(), self.original_file_name

        self.del_this_later = utils_tests_folder_path / 'del_this.ipynb'

        shutil.copy(self.original_file_name, self.del_this_later)

        if self.del_this_later.exists():
            self.input_file_name = self.del_this_later
        else:
            raise IOError('Unable to create %s' % self.del_this_later)

    def tearDown(self):
        if self.del_this_later.exists():
            self.del_this_later.unlink()

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
