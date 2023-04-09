import os
import pathlib
import sys
import tempfile
import unittest

import nbformat


sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), os.pardir
        )
    )
)


import end_with_two_returns as tr


class TestFile(unittest.TestCase):
    def setUp(self):
        self.fp = open(
            os.path.join(
                os.path.dirname(__file__), 
                'sample.ipynb'
            ), 
            encoding = 'utf-8'
        )

        self.nb = nbformat.read(self.fp, nbformat.NO_CONVERT)

        self.fp.seek(0)

        self.cell = self.nb['cells'][0]
        self.cell_src_strip = self.cell.source.strip()
    
    def tearDown(self):
        del self.cell_src_strip
        del self.cell
        del self.nb
        self.fp.close()

    def test_gen_cells(self):
        for cell in tr.gen_cells(self.fp):
            self.assertIsInstance(cell, nbformat.notebooknode.NotebookNode)

    def test_get_source_from_cell(self):
        cell = self.cell
        source = tr.get_source_from_cell(cell)
        self.assertIsInstance(source, str)

    def test_process_cell_no_return(self):
        cell = nbformat.notebooknode.NotebookNode(self.cell)
        cell.source = self.cell_src_strip
        expected = self.cell_src_strip + '\n\n'

        result = tr.process_cell(cell)

        self.assertEqual(expected, result.source,)

    def test_process_cell_one_return(self):
        cell = nbformat.notebooknode.NotebookNode(self.cell)
        cell.source = self.cell_src_strip + '\n'
        expected = self.cell_src_strip + '\n\n'

        result = tr.process_cell(cell)

        self.assertEqual(expected, result.source,)

    def test_process_cell_two_returns(self):
        cell = nbformat.notebooknode.NotebookNode(self.cell)
        cell.source = self.cell_src_strip + '\n\n'
        expected = cell.source.strip() + '\n\n'

        result = tr.process_cell(cell)

        self.assertEqual(expected, result.source,)


class TestCell(unittest.TestCase):
    def test_add_two_returns_if_missing_two_returns(self):
        source_ending_with_two_returns = 'abc\n\n'

        result = tr.add_two_returns_if_missing(source_ending_with_two_returns)

        self.assertEqual(source_ending_with_two_returns, result,)

    def test_add_two_returns_if_missing_one_return(self):
        source_ending_with_one_return = 'abc\n'

        result = tr.add_two_returns_if_missing(source_ending_with_one_return)

        self.assertEqual(source_ending_with_one_return + '\n', result,)

    def test_add_two_returns_if_missing_no_return(self):
        source_ending_without_return = 'abc'

        result = tr.add_two_returns_if_missing(source_ending_without_return)

        self.assertEqual(source_ending_without_return + '\n\n', result,)


class TestWritingFile(unittest.TestCase):
    def setUp(self):
        self.test_file_path = pathlib.Path(__file__)
        self.test_folder_path = self.test_file_path.parent.absolute()
        assert self.test_folder_path.exists(), self.test_folder_path
        assert self.test_folder_path.is_dir()

        self.input_file_path = self.test_folder_path / 'sample.ipynb'
        assert self.input_file_path.exists(), self.input_file_path
        assert self.input_file_path.is_file()

    @staticmethod
    def same_length(seq_0, seq_1):
        return len(seq_0) == len(seq_1)

    @staticmethod
    def second_one_is_longer_by_one(seq_0, seq_1):
        return (len(seq_0)+1) == len(seq_1)

    @staticmethod
    def last_one_source_is_empty(seq):
        return "" == seq[-1].source

    @staticmethod
    def last_one_source_is_whitespace_only(seq):
        return "" == seq[-1].source.strip()

    def test_process_file(self):
        # function under test
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = pathlib.Path(tmpdir)

            output_path = tmppath / self.input_file_path.name
            assert not output_path.exists()

            tr.process_file(self.input_file_path, output_path)

            nb_input = nbformat.read(self.input_file_path, nbformat.NO_CONVERT)
            nb_output = nbformat.read(output_path, nbformat.NO_CONVERT)

            self.assertGreater(len(nb_input['cells']), 0)

            if self.same_length(nb_input['cells'], nb_output['cells']):
                self.assertFalse(nb_input['cells'][-1].source)
                self.assertFalse(nb_output['cells'][-1].source)
            elif self.second_one_is_longer_by_one(nb_input['cells'], nb_output['cells']):
                self.assertTrue(nb_input['cells'][-1].source)
                self.assertFalse(nb_output['cells'][-1].source)
            else:
                raise NotImplementedError

            for in_cell, out_cell in zip(nb_input['cells'], nb_output['cells']):
                self.assertEqual(
                    in_cell.source.strip() + '\n\n',
                    out_cell.source
                )


if "__main__" == __name__:
    unittest.main()
