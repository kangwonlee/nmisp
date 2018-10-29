import re

import nbformat


def is_cell_markdown(cell):
    return cell['cell_type'].strip().lower().startswith('markdown')


def get_re_markdown_simple_link():
    return re.compile(r'\[.+?\]\((.+?)\)')


def get_re_markdown_image_link():
    return re.compile(r'\[\!\[.+?\]\(.+?\)\]\((.+?)\)')


def check_links_in_ipynb(filename):
    with open(filename, encoding='utf-8') as ipynb:
        nb = nbformat.read(ipynb, nbformat.NO_CONVERT)

    for cell in filter(is_cell_markdown, nb['cells']):
        # see if the cell has links
        print(cell['source'])
