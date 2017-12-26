import re

import nb_file_util as fu


class SymbolLister(fu.CellProcessorBase):
    def has_symbol(self):
        """
         if symbol definition line included, return the line numbers and the contents in a list

        :return: list of dict('line_number':int, 'source':str])
        """
        result = []
        if self.is_code():
            if self.has_source():
                for line_number, source_line in enumerate(self.cell['source'].splitlines()):
                    if ('sy.symbols' in source_line) or ('sy.Symbol' in source_line):
                        result.append({'line number': line_number, 'source': source_line})

        return result

    def process_cell(self):
        return self.has_symbol()


class SymbolConverter(SymbolLister):
    """
    sy.symbols('L_AB_m', real=True, nonnegative=True) -> sy.symbols('L_{AB}[m]', real=True, nonnegative=True)
    sy.symbols('w0_N_m', real=True) -> sy.symbols('w0[N/m]', real=True)

    'L_AB_m' -> [wrap_symbol_name] -> 'L_{AB}_{m}' -> 'L_{AB}[m]'

    """
    units_set = {'m', 'mm', 'mm3', 'm2', 'm3', 'm4', 'deg', 'rad', 'N', 'Nm', 'N_m', 'Pa', 'MPa', 'm_s2', 'kg'}

    def __init__(self):
        super().__init__()
        self.conversion_table_dict = self.unit_underline_wrap_bracket()

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

    # def process_cell(self):
    #     symbol_list = self.has_symbol()
    #     # [{'line number': int, 'source': str}]
    #
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

        first_attempt = re.search('.*\.(Symbol|symbols)\s*\([\'\"]', source_line)
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
        for to_be_replaced in self.conversion_table_dict:
            if text_to_apply.endswith(to_be_replaced):
                new_small_dict[original_symbol_name] = text_to_apply.replace(to_be_replaced,
                                                                             lookup_table_dict[to_be_replaced])
                # if lookup table original_symbol_name found, break lookup table loop
                break

        return new_small_dict


def symbol_lines_in_file(input_file_name):
    sc = SymbolLister()
    file_processor = fu.FileProcessor(input_file_name, sc)
    result = file_processor.process_nb_file()

    return result
