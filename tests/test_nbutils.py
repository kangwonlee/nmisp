import subprocess
import unittest

import ipynb_remove_output as nbutils

null = dir(nbutils)


class TestNButils(unittest.TestCase):
    def setUp(self):
        self.input_file_name = 'sample.ipynb'

    def test_sample_ipynb(self):
        # should run without an exception
        _exec_notebook(self.input_file_name)

    def test_read_notebook(self):
        result = nbutils.read_file(self.input_file_name)
        self.assertIn('cells', result)
        self.assertIn('nbformat', result)
        self.assertIn('nbformat_minor', result)

    def test_has_symbol(self):
        file = nbutils.read_file(self.input_file_name)
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
        file = nbutils.read_file(self.input_file_name)
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


def _exec_notebook(path):
    # http://nbconvert.readthedocs.io/en/latest/execute_api.html
    # ijstokes et al, Command line execution of a jupyter notebook fails in default Anaconda 4.1, https://github.com/Anaconda-Platform/nb_conda_kernels/issues/34
    args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
            "--ExecutePreprocessor.timeout=1000",
            "--ExecutePreprocessor.kernel_name=python", path]
    subprocess.check_call(args)


if __name__ == '__main__':
    unittest.main()
    # finished running
