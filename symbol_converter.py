import nb_file_util as fu


def symbol_lines_in_file(input_file_name):
    file_processor = fu.FileProcessor(input_file_name)
    result = file_processor.process_nb_file()

    return result
