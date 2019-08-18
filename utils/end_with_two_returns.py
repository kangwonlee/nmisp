import os

import nbformat


def get_cur_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_par_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def gen_items(path):
    for item in os.listdir(path):
        path_item = os.path.abspath(os.path.join(path, item))
        assert os.path.exists(path_item), f"Missing : {path_item}"
        yield path_item


def gen_folders(path=get_par_dir()):
    for item in gen_items(path):
        if os.path.isdir(item):
            yield item


def gen_files(path, ext='ipynb'):
    for item in gen_items(path):
        if os.path.isfile(item):
            if os.path.splitext(item)[-1].endswith(ext):
                yield item


def gen_ipynb_files_above(path=get_par_dir(), ext='ipynb'):
    for folder in gen_folders(path):
        for file in gen_files(folder, ext):
            yield file


def gen_cells(ipynb_file):
    nb = nbformat.read(ipynb_file, nbformat.NO_CONVERT)

    for cell in nb['cells']:
        yield cell


def get_source_from_cell(cell):
    assert isinstance(cell, nbformat.notebooknode.NotebookNode), repr(cell)
    return cell['source']


def add_two_returns_if_missing(cell_source):
    if cell_source.endswith('\n\n'):
        pass
    elif cell_source.endswith('\n'):
        cell_source += '\n'
    else:
        cell_source += '\n\n'

    return cell_source


def process_cell(cell):
    cell['source'] = add_two_returns_if_missing(
        get_source_from_cell(cell)
    )

    return cell


def process_file(input_ipynb_filename, output_ipynb_filename=None):

    if output_ipynb_filename is None:
        output_ipynb_filename = input_ipynb_filename

    nb = nbformat.read(input_ipynb_filename, nbformat.NO_CONVERT)

    for cell in nb['cells']:
        process_cell(cell)

    nb['cells'][-1].source = ""

    nbformat.write(nb, output_ipynb_filename)


def main():
    for ipynb_file in gen_ipynb_files_above():
        print(f'processing {ipynb_file}', end=' ')
        process_file(ipynb_file)
        print('done')


if "__main__" == __name__:
    main()
