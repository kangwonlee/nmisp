import nb_file_util as fu


class SymbolConverter(fu.CellProcessorBase):
    def process_cell(self):
        return self.has_symbol()


def symbol_lines_in_file(input_file_name):
    file_processor = fu.FileProcessor(input_file_name)
    result = file_processor.process_nb_file()

    return result
