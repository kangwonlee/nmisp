import os
import sys
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
    
    def tearDown(self):
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
        cell = self.cell
        cell.source = cell.source.strip()
        expected = cell.source.strip() + '\n\n'

        result = tr.process_cell(cell)

        self.assertEqual(result.source, expected)

    def test_process_cell_one_return(self):
        cell = self.cell
        cell.source = cell.source.strip() + '\n'
        expected = cell.source.strip() + '\n\n'

        result = tr.process_cell(cell)

        self.assertEqual(result.source, expected)

    def test_process_cell_two_returns(self):
        cell = self.cell
        cell.source = cell.source.strip() + '\n\n'
        expected = cell.source.strip() + '\n\n'

        result = tr.process_cell(cell)

        self.assertEqual(result.source, expected)


class TestCell(unittest.TestCase):
    def test_add_two_returns_if_missing_two_returns(self):
        source_ending_with_two_returns = 'abc\n\n'

        result = tr.add_two_returns_if_missing(source_ending_with_two_returns)

        self.assertEqual(result, source_ending_with_two_returns)

    def test_add_two_returns_if_missing_one_return(self):
        source_ending_with_one_return = 'abc\n'

        result = tr.add_two_returns_if_missing(source_ending_with_one_return)

        self.assertEqual(result, source_ending_with_one_return + '\n')

    def test_add_two_returns_if_missing_no_return(self):
        source_ending_without_return = 'abc'

        result = tr.add_two_returns_if_missing(source_ending_without_return)

        self.assertEqual(result, source_ending_without_return + '\n\n')


if "__main__" == __name__:
    unittest.main()
