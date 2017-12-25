import unittest

import ipynb_remove_output as nbutils


class TestRemoveOutput(unittest.TestCase):
    def setUp(self):
        self.input_file_name = 'sample.ipynb'

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
