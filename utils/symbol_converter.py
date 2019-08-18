import os
import re
import sys


sys.path.append(os.path.dirname(__file__))

import nb_file_util as fu


class SymbolLister(fu.CellProcessorBase):
    def calls_sympy_symbol(self):
        """
         if symbol definition line included, return the line numbers and the contents in a list

        :return: list of dict('line_number':int, 'source':str])
        """

        # TODO : What if import sympy
        # TODO : Consider using ast module

        result = []
        if self.is_code():
            if self.has_source():
                for line_number, source_line in enumerate(self.cell['source'].splitlines()):
                    if ('sy.symbols' in source_line) or ('sy.Symbol' in source_line):
                        result.append({'line number': line_number, 'source': source_line})

        return result

    def process_cell(self):
        return self.calls_sympy_symbol()


class SymbolConverter(SymbolLister):
    """
    sy.symbols('L_AB_m', real=True, nonnegative=True) -> sy.symbols('L_{AB}[m]', real=True, nonnegative=True)
    sy.symbols('w0_N_m', real=True) -> sy.symbols('w0[N/m]', real=True)

    "L_AB_m, L_AC_m = sy.symbols('L_AB_m, L_AC_m', real=True, nonnegative=True)"
    -> [find symbol location] -> 'L_AB_m, L_AC_m' ->
    'L_AB_m' -> [wrap_symbol_name] -> 'L_{AB}_{m}' -> 'L_{AB}[m]'

    """
    units_set = {'m', 'mm', 'mm3', 'm2', 'm3', 'm4', 'deg', 'rad', 'N', 'Nm', 'N_m', 'Pa', 'MPa', 'm_s2', 'kg'}

    def __init__(self):
        super().__init__()
        self.conversion_table_dict = self.unit_underline_wrap_bracket()
        self.secondary_table_dict = self.make_secondary_table()
        self.re_split = self.prepare_split_rule()

    @staticmethod
    def make_secondary_table():
        return {
            '_{N}[m]': '[N/m]',
            '_{N}[mm]': '[N/mm]',
            '_{N}[m^{2}]': '[N/m^{2}]',
            '_{N}[mm^{2}]': '[N/mm^{2}]',
        }

    @staticmethod
    def prepare_split_rule():
        return re.compile(r'[, ]')

    @staticmethod
    def wrap_symbol_name(symbol_name):
        """
        Wrap '_' separated symbol name parts with '{}'
        :param str symbol_name:
        :return:

        Example
        >>> cp = SymbolConverter()
        >>> cp.wrap_symbol_name('L_AB_m')
        'L_{AB}_{m}'
        """
        symbol_name_split_under_line = symbol_name.split('_')
        if 1 < len(symbol_name_split_under_line):
            symbol_name_underline_wrapped = [symbol_name_split_under_line[0]]
            for part in symbol_name_split_under_line[1:]:
                symbol_name_underline_wrapped.append('{%s}' % part)

            symbol_name = '_'.join(symbol_name_underline_wrapped)

        return symbol_name

    def unit_underline_wrap_bracket(self):
        """
        '_{m_s2}': '[m/s^{2}]'
        '_{N_m}': '[N/m]'

        :return: dictionary
        :rtype dict
        """
        conversion_table_dict = {}
        for unit in self.units_set:
            key = '_{%s}' % unit
            value = '[%s]' % unit.replace('_', '/').replace('4', '^{4}').replace('3', '^{3}').replace('2', '^{2}')

            conversion_table_dict[key] = value

        return conversion_table_dict

    def process_cell(self):
        source_lines = self.cell['source'].splitlines()

        symbol_list = self.calls_sympy_symbol()
        # [{'line number': int, 'source': str}]

        for symbol_line in symbol_list:
            converted_line = self.process_line(symbol_line['source'])
            # replace the source code with the new line
            source_lines[symbol_line['line number']] = converted_line

        converted_source_code = '\n'.join(source_lines)

        if self.cell['source'] and '\n' == self.cell['source'][-1]:
            converted_source_code += '\n'

        # update cell
        self.cell['source'] = converted_source_code

    def process_line(self, source_line):
        """
        SymbolConverter.process_line()

        Find SymPy 
        """

        symbol_names_location = self.find_symbol_name_location(source_line)
        symbol_names_str = source_line[symbol_names_location[0]:symbol_names_location[1]]
        symbol_names_list = filter(lambda x: bool(x),
                                   [symbol_name.strip() for symbol_name in self.re_split.split(symbol_names_str)])
        converted_symbol_names_list = [self.process_symbol_name(symbol_name) for symbol_name in symbol_names_list]
        converted_symbol_names_str = ', '.join(converted_symbol_names_list)
        converted_source_line = (source_line[:symbol_names_location[0]]
                                 + converted_symbol_names_str
                                 + source_line[symbol_names_location[1]:])
        return converted_source_line

    def process_symbol_name(self, symbol_name):
        result = {symbol_name:symbol_name}
        wrapped = self.wrap_symbol_name(symbol_name)
        # first conversion layer : for majority of cases
        result.update(self.apply_lookup_table(wrapped, symbol_name))
        # second conversion layer : for N/m, N/m^{2} cases
        result.update(self.apply_lookup_table(result[symbol_name], symbol_name, self.secondary_table_dict))
        return result[symbol_name]

    def find_symbol_name_location(self, source_line):
        """

        :param str source_line:
        :return: (int, int)

        >>> cp = SymbolConverter()
        >>> source_line = "L_AB_m = sy.symbols('L_AB_m', real=True, nonnegative=True)"
        >>> result = cp.find_symbol_name_location(source_line)
        >>> source_line[result[0]:result[1]]
        'L_AB_m'
        >>> source_line = "L_AB_m = sy.Symbol('L_AB_m', real=True, nonnegative=True)"
        >>> result = cp.find_symbol_name_location(source_line)
        >>> source_line[result[0]:result[1]]
        'L_AB_m'
        "'"
        """

        first_attempt = re.search(r'.*\.(Symbol|symbols)\s*\([\'\"]', source_line)
        quote = source_line[first_attempt.regs[0][1] - 1]
        quote_pattern = chr(92) + quote  # backslash + ['"]
        second_attempt = re.search(r'.*\.(Symbol|symbols)\s*\(' + quote_pattern + r'(.+?)' + quote_pattern, source_line)

        if first_attempt:
            start = first_attempt.regs[0][1]
            end = second_attempt.regs[0][1] - 1
            result = (start, end)
        else:
            result = None

        return result

    def apply_lookup_table(self, text_to_apply, original_symbol_name, lookup_table_dict=None):
        if lookup_table_dict is None:
            lookup_table_dict = self.conversion_table_dict

        new_small_dict = {}
        # lookup table loop
        for to_be_replaced in lookup_table_dict:
            if text_to_apply.endswith(to_be_replaced):
                new_small_dict[original_symbol_name] = text_to_apply.replace(to_be_replaced,
                                                                             lookup_table_dict[to_be_replaced])
                # if lookup table original_symbol_name found, break lookup table loop
                break

        return new_small_dict


class IpynbUnitConverter(fu.FileProcessor):
    def __init__(self, nb_filename):
        super().__init__(nb_filename=nb_filename, cell_processor=SymbolConverter())


def symbol_lines_in_file(input_file_name):
    sc = SymbolLister()
    file_processor = fu.FileProcessor(input_file_name, sc)
    result = file_processor.process_nb_file()

    return result
