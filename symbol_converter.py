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
    units_set = {'m', 'mm', 'mm3', 'm2', 'm3', 'm4', 'deg', 'rad', 'N', 'Nm', 'N_m', 'Pa', 'MPa', 'm_s2', 'kg'}

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
        conversion_table_dict = {}
        for unit in self.units_set:
            key = '_{%s}' % unit
            value = '[%s]' % unit.replace('_', '/').replace('4', '^{4}').replace('3', '^{3}').replace('2', '^{2}')

            conversion_table_dict[key] = value

        return conversion_table_dict


def symbol_lines_in_file(input_file_name):
    sc = SymbolLister()
    file_processor = fu.FileProcessor(input_file_name, sc)
    result = file_processor.process_nb_file()

    return result
