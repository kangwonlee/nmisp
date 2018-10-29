import re
import urllib.request as ur

import nbformat


def is_cell_markdown(cell):
    return cell['cell_type'].strip().lower().startswith('markdown')


def get_re_markdown_simple_link():
    return re.compile(r'\[.+?\]\((.+?)\)')


def get_re_markdown_image_link():
    return re.compile(r'\[\!\[.+?\]\(.+?\)\]\((.+?)\)')


ri = get_re_markdown_image_link()
rs = get_re_markdown_simple_link()

def check_link_in_cell(cell, r):
    for m in r.finditer(cell['source']):
        with ur.urlopen(m.group(1)) as _:
            pass


def check_links_in_ipynb(filename):
    with open(filename, encoding='utf-8') as ipynb:
        nb = nbformat.read(ipynb, nbformat.NO_CONVERT)

    for cell in filter(is_cell_markdown, nb['cells']):
        # see if the cell has links
        # https://stackoverflow.com/questions/16778435/python-check-if-website-exists
        check_link_in_cell(cell, rs)
        check_link_in_cell(cell, ri)
