import re
import urllib.parse as up
import urllib.request as ur

import nbformat
import requests


def is_cell_markdown(cell):
    """
    Is the ipynb cell Markdown?
    """
    return cell['cell_type'].strip().lower().startswith('markdown')


def get_re_markdown_simple_link():
    """
    Regular Expression to find markdown urls
    [text](url)
    """
    return re.compile(r'\[.+?\]\((.+?)\)')


def get_re_markdown_image_link():
    """
    Regular Expression to find urls linked to images
    [![text](image url)](url)
    """
    return re.compile(r'\[\!\[.+?\]\(.+?\)\]\((.+?)\)')


# to avoid compiling repetitively
ri = get_re_markdown_image_link()
rs = get_re_markdown_simple_link()

def check_link_in_cell(cell, r):
    """
    cell : ipynb cell
    r : regex. return value from get_re_markdown_simple_link() or get_re_markdown_image_link()
    """
    # url match loop
    for m in r.finditer(cell['source']):
        # try to open url part of the match
        req = requests.get(up.unquote(m.group(1)))
        if 200 == req.status_code:
            result = True
        else:
            raise requests.RequestException(f'unable to get {up.unquote(m.group(1))}')


def check_links_in_ipynb(filename):
    """
    filename : path to an ipynb file
    """
    # open file and read
    with open(filename, encoding='utf-8') as ipynb:
        nb = nbformat.read(ipynb, nbformat.NO_CONVERT)

    check_links_in_ipynb_cells_list(nb['cells'])


def check_links_in_ipynb_cells_list(cells_list):
    """
    cells_list : ipynb notebook's cells

    >>> with open(filename, encoding='utf-8') as ipynb:
        nb = nbformat.read(ipynb, nbformat.NO_CONVERT)
    >>> check_links_in_ipynb_cells_list(nb['cells'])
    """
    # cell loop
    for cell in filter(is_cell_markdown, cells_list):
        # see if the cell has links
        # https://stackoverflow.com/questions/16778435/python-check-if-website-exists

        # check simple urls
        check_link_in_cell(cell, rs)
        # check urls linked to 
        check_link_in_cell(cell, ri)
