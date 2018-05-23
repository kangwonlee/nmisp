import os
import unittest

import nb_file_util as nbutils

null = dir(nbutils)


class TestNotebookFileUtil(unittest.TestCase):
    def setUp(self):
        self.input_file_name = os.path.join('tests', 'sample.ipynb')
        self.file_processor = nbutils.FileProcessor(self.input_file_name)

    def test_use_default_filename_if_missing(self):
        self.assertTrue(os.path.exists(self.file_processor.use_default_filename_if_missing(None)))

    def test_sample_ipynb(self):
        # should run without an exception
        self.file_processor.execute()

    def test_read_notebook(self):
        result = self.file_processor.read_file()
        self.assertIn('cells', result)
        self.assertIn('nbformat', result)
        self.assertIn('nbformat_minor', result)


if __name__ == '__main__':
    unittest.main()
    # finished running
