import pathlib
import unittest

import nb_file_util as nbutils

null = dir(nbutils)


class TestNotebookFileUtil(unittest.TestCase):
    def setUp(self):
        self.input_file_name = pathlib.Path(__file__).parent.absolute() / 'sample.ipynb'
        assert self.input_file_name.exists(), self.input_file_name
        self.file_processor = nbutils.FileProcessor(self.input_file_name)

    def test_use_default_filename_if_missing(self):
        assert pathlib.Path(self.file_processor.use_default_filename_if_missing(None)).exists()

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
