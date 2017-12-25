import nb_file_util as fu


class SymbolConverter(fu.CellProcessorBase):
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


def symbol_lines_in_file(input_file_name):
    sc = SymbolConverter()
    file_processor = fu.FileProcessor(input_file_name, sc)
    result = file_processor.process_nb_file()

    return result
