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
        file = self.file_processor.read_file()
        cells = file['cells']
        result = []
        for k, cell in enumerate(cells):
            cell_result = nbutils.has_symbol(cell)
            if cell_result:
                result.append((k, cell_result))

        # compare with an expected list
        expected = [(8, [(0, "L_AB_m = sy.symbols('L_AB_m', real=True, nonnegative=True)")]),
                    (10, [(0, "w0_N_m = sy.symbols('w0_N_m', real=True)")]),
                    (12, [(0, "E_Pa, I_m4 = sy.symbols('E_Pa, I_m4', positive=True)")]),
                    (14, [(0, "x_m = sy.symbols('x_m', nonnegative=True)")]),
                    (16, [(0, "R_A_N, M_A_Nm, R_B_N = sy.symbols('R_A_N, M_A_Nm, R_B_N', real=True)")])]

        self.assertSequenceEqual(expected, result)

    def test_cells_with_symbol(self):
        result = nbutils.symbol_lines_in_file(self.input_file_name)

        # compare with an expected list
        expected = [(8, [(0, "L_AB_m = sy.symbols('L_AB_m', real=True, nonnegative=True)")]),
                    (10, [(0, "w0_N_m = sy.symbols('w0_N_m', real=True)")]),
                    (12, [(0, "E_Pa, I_m4 = sy.symbols('E_Pa, I_m4', positive=True)")]),
                    (14, [(0, "x_m = sy.symbols('x_m', nonnegative=True)")]),
                    (16, [(0, "R_A_N, M_A_Nm, R_B_N = sy.symbols('R_A_N, M_A_Nm, R_B_N', real=True)")])]

        self.assertSequenceEqual(expected, result)

    def test_replace_symbol(self):
        file = self.file_processor.read_file()
        cells = file['cells']
        result = []
        for k, cell in enumerate(cells):
            cell_result = nbutils.has_symbol(cell)
            if cell_result:
                result.append((k, cell_result))

        # compare with an expected list
        expected = [(8, [(0, "L_AB_m = sy.symbols('L_{AB}[m]', real=True, nonnegative=True)")]),
                    (10, [(0, "w0_N_m = sy.symbols('w0[N/m]', real=True)")]),
                    (12, [(0, "E_Pa, I_m4 = sy.symbols('E[Pa], I[m^{4}]', positive=True)")]),
                    (14, [(0, "x_m = sy.symbols('x[m]', nonnegative=True)")]),
                    (16, [(0, "R_A_N, M_A_Nm, R_B_N = sy.symbols('R_{A}[N], M_{A}[Nm], R_{B}[N]', real=True)")])]

        self.assertSequenceEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
    # finished running
