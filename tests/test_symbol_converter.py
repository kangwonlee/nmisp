import os
import unittest

import nb_file_util as fu
import symbol_converter as sc


class TestSymbolLister(unittest.TestCase):
    def setUp(self):
        self.input_file_name = os.path.join('tests', 'sample.ipynb')
        self.file_processor = fu.FileProcessor(self.input_file_name)

        # class under test
        self.cp = sc.SymbolLister()

    def test_cells_with_symbol(self):
        self.maxDiff = None
        result = sc.symbol_lines_in_file(self.input_file_name)

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

    def test_calls_sympy_symbol(self):
        self.maxDiff = None

        file = self.file_processor.read_file()
        cells = file['cells']
        result = []

        for k, cell in enumerate(cells):
            self.cp.set_cell(cell)
            # function under test
            cell_result = self.cp.calls_sympy_symbol()
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


class MyLineConverterTesterBase(unittest.TestCase):
    def setUp(self):
        self.input_file_name = os.path.join('tests', 'sample.ipynb')

        # class under test
        self.cp = sc.SymbolConverter()

        self.file_processor = fu.FileProcessor(self.input_file_name, self.cp)

    def check_process_line(self, source_line, expected):
        result = self.cp.process_line(source_line)
        self.assertEqual(expected, result)

        # test run the converted statement
        result_sy = exec('''import sympy as sy
%s''' % result)
        self.assertIsNone(result_sy)


class TestSymbolConverter(MyLineConverterTesterBase):
    def test_wrap_symbol_name(self):
        result = self.cp.wrap_symbol_name('L_AB_m')
        expected = 'L_{AB}_{m}'

        self.assertEqual(expected, result)

    def test_unit_underline_wrap_bracket(self):
        self.maxDiff = None
        result = self.cp.unit_underline_wrap_bracket()
        expected = {'_{mm}': '[mm]', '_{MPa}': '[MPa]', '_{mm3}': '[mm^{3}]', '_{kg}': '[kg]', '_{m3}': '[m^{3}]',
                    '_{rad}': '[rad]', '_{m_s2}': '[m/s^{2}]', '_{N}': '[N]', '_{deg}': '[deg]', '_{Pa}': '[Pa]',
                    '_{m2}': '[m^{2}]', '_{m4}': '[m^{4}]', '_{Nm}': '[Nm]', '_{m}': '[m]', '_{N_m}': '[N/m]'}
        self.assertDictEqual(expected, result)

    def test_find_symbol_name_location_00(self):
        #              0         1         2
        #              0123456789012345678901234567890123456789012345678901234567890123456789
        #                                     0123456789012345678901234567890123456789012345678901234567890123456789
        source_line = "L_AB_m = sy.symbols('L_AB_m', real=True, nonnegative=True)"
        result = self.cp.find_symbol_name_location(source_line)
        extracted = source_line[result[0]:result[1]]
        expected_extracted = 'L_AB_m'

        self.assertEqual(expected_extracted, extracted)

    def test_find_symbol_name_location_01(self):
        #              0         1         2
        #              0123456789012345678901234567890123456789012345678901234567890123456789
        #                                   0123456789012345678901234567890123456789012345678901234567890123456789
        source_line = "L_AB = sy.symbols('L_AB_m', real=True, nonnegative=True)"
        result = self.cp.find_symbol_name_location(source_line)
        extracted = source_line[result[0]:result[1]]
        expected_extracted = 'L_AB_m'

        self.assertEqual(expected_extracted, extracted)

    def test_find_symbol_name_location_10(self):
        #              0         1         2
        #              0123456789012345678901234567890123456789012345678901234567890123456789
        #                                     0123456789012345678901234567890123456789012345678901234567890123456789
        source_line = "L_AB_m = sy.Symbol('L_AB_m', real=True, nonnegative=True)"
        result = self.cp.find_symbol_name_location(source_line)
        extracted = source_line[result[0]:result[1]]
        expected_extracted = 'L_AB_m'

        self.assertEqual(expected_extracted, extracted)

    def test_find_symbol_name_location_11(self):
        #              0         1         2
        #              0123456789012345678901234567890123456789012345678901234567890123456789
        #                                   0123456789012345678901234567890123456789012345678901234567890123456789
        source_line = "L_AB = sy.Symbol('L_AB_m', real=True, nonnegative=True)"
        result = self.cp.find_symbol_name_location(source_line)
        extracted = source_line[result[0]:result[1]]
        expected_extracted = 'L_AB_m'

        self.assertEqual(expected_extracted, extracted)

    def test_find_symbol_name_location_100(self):
        #              0         1         2
        #              0123456789012345678901234567890123456789012345678901234567890123456789
        #                                     0123456789012345678901234567890123456789012345678901234567890123456789
        source_line = "L_AB_m, L_AC_m = sy.symbols('L_AB_m, L_AC_m', real=True, nonnegative=True)"
        result = self.cp.find_symbol_name_location(source_line)
        extracted = source_line[result[0]:result[1]]
        expected_extracted = 'L_AB_m, L_AC_m'

        self.assertEqual(expected_extracted, extracted)

    def test_find_symbol_name_location_101(self):
        #              0         1         2
        #              0123456789012345678901234567890123456789012345678901234567890123456789
        #                                   0123456789012345678901234567890123456789012345678901234567890123456789
        source_line = "L_AB, L_AC_m = sy.symbols('L_AB_m, L_AC_m', real=True, nonnegative=True)"
        result = self.cp.find_symbol_name_location(source_line)
        extracted = source_line[result[0]:result[1]]
        expected_extracted = 'L_AB_m, L_AC_m'

        self.assertEqual(expected_extracted, extracted)

    def test_process_line_00(self):
        self.check_process_line("L_AB_m = sy.symbols('L_AB_m', real=True, nonnegative=True)",
                                "L_AB_m = sy.symbols('L_{AB}[m]', real=True, nonnegative=True)")

    def test_process_line_01(self):
        #              0         1         2
        #              0123456789012345678901234567890123456789012345678901234567890123456789
        #                                   0123456789012345678901234567890123456789012345678901234567890123456789
        self.check_process_line("L_AB = sy.symbols('L_AB_m', real=True, nonnegative=True)",
                                "L_AB = sy.symbols('L_{AB}[m]', real=True, nonnegative=True)")

    def test_process_line_10(self):
        #              0         1         2
        #              0123456789012345678901234567890123456789012345678901234567890123456789
        #                                     0123456789012345678901234567890123456789012345678901234567890123456789
        self.check_process_line("L_AB_m = sy.Symbol('L_AB_m', real=True, nonnegative=True)",
                                "L_AB_m = sy.Symbol('L_{AB}[m]', real=True, nonnegative=True)")

    def test_process_line_11(self):
        self.check_process_line("L_AB = sy.Symbol('L_AB_m', real=True, nonnegative=True)",
                                "L_AB = sy.Symbol('L_{AB}[m]', real=True, nonnegative=True)")

    def test_process_line_100(self):
        self.check_process_line("L_AB_m, L_AC_m = sy.symbols('L_AB_m, L_AC_m', real=True, nonnegative=True)",
                                "L_AB_m, L_AC_m = sy.symbols('L_{AB}[m], L_{AC}[m]', real=True, nonnegative=True)")

    def test_process_line_101(self):
        self.check_process_line("L_AB, L_AC_m = sy.symbols('L_AB_m, L_AC_m', real=True, nonnegative=True)",
                                "L_AB, L_AC_m = sy.symbols('L_{AB}[m], L_{AC}[m]', real=True, nonnegative=True)")

    def test_process_line_110(self):
        self.check_process_line("L_AB_m, L_AC_m = sy.symbols('L_AB_m, L_AC_m', real=True, nonnegative=True)",
                                "L_AB_m, L_AC_m = sy.symbols('L_{AB}[m], L_{AC}[m]', real=True, nonnegative=True)")

    def test_process_line_111(self):
        self.check_process_line("L_AB, L_AC_m = sy.symbols('L_AB_m, L_AC_m', real=True, nonnegative=True)",
                                "L_AB, L_AC_m = sy.symbols('L_{AB}[m], L_{AC}[m]', real=True, nonnegative=True)")

    def test_cell_processor(self):
        file = self.file_processor.read_file()

        cells = file['cells']

        for k, cell in enumerate(cells):
            self.cp.set_cell(cell)
            # function under test
            self.cp.process_cell()

        # begin read processed result
        result = []

        for k, cell in enumerate(cells):
            self.cp.set_cell(cell)
            # function under test
            cell_result = self.cp.calls_sympy_symbol()
            if cell_result:
                result.append((k, cell_result))

        expected = [
            (8, [{'line number': 0, 'source': "L_AB_m = sy.symbols('L_{AB}[m]', real=True, nonnegative=True)"}]),
            (10, [{'line number': 0, 'source': "w0_N_m = sy.symbols('w0[N/m]', real=True)"}]),
            (12, [{'line number': 0, 'source': "E_Pa, I_m4 = sy.symbols('E[Pa], I[m^{4}]', positive=True)"}]),
            (14, [{'line number': 0, 'source': "x_m = sy.symbols('x[m]', nonnegative=True)"}]), (16, [{'line number': 0,
                                                                                                       'source': "R_A_N, M_A_Nm, R_B_N = sy.symbols('R_{A}[N], M_{A}[Nm], R_{B}[N]', real=True)"}])]

        # end reading processed result
        self.assertSequenceEqual(expected, result)


class TestSymbolConverter00(MyLineConverterTesterBase):
    def test_process_line_00(self):
        self.check_process_line("w0_N_m = sy.symbols('w0_N_m', real=True)",
                                "w0_N_m = sy.symbols('w0[N/m]', real=True)")

    def test_process_line_01(self):
        self.check_process_line("w0_N = sy.symbols('w0_N_m', real=True)",
                                "w0_N = sy.symbols('w0[N/m]', real=True)")

    def test_process_line_10(self):
        self.check_process_line("w0_N_m = sy.Symbol('w0_N_m', real=True)",
                                "w0_N_m = sy.Symbol('w0[N/m]', real=True)")

    def test_process_line_11(self):
        self.check_process_line("w0_N = sy.Symbol('w0_N_m', real=True)",
                                "w0_N = sy.Symbol('w0[N/m]', real=True)")


class TestSymbolConverter01(MyLineConverterTesterBase):
    def test_process_line_00(self):
        self.check_process_line("E_Pa, I_m4 = sy.symbols('E_Pa, I_m4', positive=True)",
                                "E_Pa, I_m4 = sy.symbols('E[Pa], I[m^{4}]', positive=True)")

    def test_process_line_01(self):
        self.check_process_line("E, I = sy.symbols('E_Pa, I_m4', positive=True)",
                                "E, I = sy.symbols('E[Pa], I[m^{4}]', positive=True)")

    def test_process_line_10(self):
        self.check_process_line("x_m = sy.symbols('x_m', nonnegative=True)",
                                "x_m = sy.symbols('x[m]', nonnegative=True)")

    def test_process_line_20(self):
        self.check_process_line("R_A_N, M_A_Nm, R_B_N = sy.symbols('R_A_N, M_A_Nm, R_B_N', real=True)",
                                "R_A_N, M_A_Nm, R_B_N = sy.symbols('R_{A}[N], M_{A}[Nm], R_{B}[N]', real=True)")
