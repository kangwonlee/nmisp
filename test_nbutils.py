import unittest

import ipynb_remove_output as nbutils

null = dir(nbutils)


class TestNButils(unittest.TestCase):
    def setUp(self):
        self.input_file_name = 'sample.ipynb'
        self.file_processor = nbutils.FileProcessor(self.input_file_name)

    def test_sample_ipynb(self):
        # should run without an exception
        self.file_processor.execute()

    def test_read_notebook(self):
        result = self.file_processor.read_file()
        self.assertIn('cells', result)
        self.assertIn('nbformat', result)
        self.assertIn('nbformat_minor', result)

    def test_has_symbol(self):
        self.maxDiff = None

        file = self.file_processor.read_file()
        cells = file['cells']
        result = []

        cp = nbutils.CellProcessor()

        for k, cell in enumerate(cells):
            cp.set_cell(cell)
            cell_result = cp.has_symbol()
            if cell_result:
                result.append((k, cell_result))

        # compare with an expected list
        expected = [(8, [{'line number': 0, 'source': "L_AB_m = sy.symbols('L_AB_m', real=True, nonnegative=True)"}]),
                    (10, [{'line number': 0, 'source': "w0_N_m = sy.symbols('w0_N_m', real=True)"}]),
                    (12, [{'line number': 0, 'source': "E_Pa, I_m4 = sy.symbols('E_Pa, I_m4', positive=True)"}]),
                    (14, [{'line number': 0, 'source': "x_m = sy.symbols('x_m', nonnegative=True)"}]),
                    (16, [{'line number': 0,
                           'source': "R_A_N, M_A_Nm, R_B_N = sy.symbols('R_A_N, M_A_Nm, R_B_N', real=True)"}])]

        self.assertSequenceEqual(expected, result)

    def test_cells_with_symbol(self):
        self.maxDiff = None
        result = nbutils.symbol_lines_in_file(self.input_file_name)

        # compare with an expected list
        expected_result = [{'cell number': 8, 'result': [
            {'line number': 0, 'source': "L_AB_m = sy.symbols('L_AB_m', real=True, nonnegative=True)"}]},
                           {'cell number': 10,
                            'result': [{'line number': 0, 'source': "w0_N_m = sy.symbols('w0_N_m', real=True)"}]},
                           {'cell number': 12, 'result': [
                               {'line number': 0, 'source': "E_Pa, I_m4 = sy.symbols('E_Pa, I_m4', positive=True)"}]},
                           {'cell number': 14,
                            'result': [{'line number': 0, 'source': "x_m = sy.symbols('x_m', nonnegative=True)"}]},
                           {'cell number': 16, 'result': [{'line number': 0,
                                                           'source': "R_A_N, M_A_Nm, R_B_N = sy.symbols('R_A_N, M_A_Nm, R_B_N', real=True)"}]}]
        expected = {'file name': self.input_file_name,
                    'result': expected_result}

        self.assertDictEqual(expected, result)

    def test_replace_symbol(self):
        self.maxDiff = None
        file = self.file_processor.read_file()
        cells = file['cells']
        result = []

        cp = nbutils.CellProcessor()

        for k, cell in enumerate(cells):
            cp.set_cell(cell)
            cell_result = cp.has_symbol()
            if cell_result:
                result.append((k, cell_result))

        # compare with an expected list
        expected = [
            (8, [{'line number': 0, 'source': "L_AB_m = sy.symbols('L_{AB}[m]', real=True, nonnegative=True)"}]),
            (10, [{'line number': 0, 'source': "w0_N_m = sy.symbols('w0[N/m]', real=True)"}]),
            (12, [{'line number': 0, 'source': "E_Pa, I_m4 = sy.symbols('E[Pa], I[m^{4}]', positive=True)"}]),
            (14, [{'line number': 0, 'source': "x_m = sy.symbols('x[m]', nonnegative=True)"}]),
            (16, [{'line number': 0,
                   'source': "R_A_N, M_A_Nm, R_B_N = sy.symbols('R_{A}[N], M_{A}[Nm], R_{B}[N]', real=True)"}])]

        self.assertSequenceEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
    # finished running
