import functools
import os
import pathlib
import re
import urllib.parse as up
import urllib.request as ur
from typing import Dict, List

import nbformat
import requests


def is_cell_markdown(cell):
    """
    Is the ipynb cell Markdown?
    """
    return cell['cell_type'].strip().lower().startswith('markdown')


@functools.lru_cache(maxsize=1)
def get_re_markdown_simple_link():
    """
    Regular Expression to find markdown urls
    [text](url)
    """
    return re.compile(r'\[.+?\]\((.+?)\)')


@functools.lru_cache(maxsize=1)
def get_re_markdown_image_link():
    """
    Regular Expression to find urls linked to images
    [![text](image url)](url)
    """
    return re.compile(r'\[\!\[.+?\]\(.+?\)\]\((.+?)\)')


def check_link_in_cell(cell, r, just_tested:List[str]=[]):
    """
    cell : ipynb cell
    r : regex. return value from get_re_markdown_simple_link() or get_re_markdown_image_link()
    """
    # url match loop
    for m in r.finditer(cell['source']):
        # try to open url part of the match

        url = up.unquote(m.group(1))

        if url in just_tested:
            continue

        just_tested.append(url)

        parsed = up.urlparse(url)

        if parsed.netloc.endswith('wikimedia.org'):
            header = get_header()
        elif (
            (os.environ.get('CI', 'false').lower() == 'true') and
            (
                parsed.netloc.endswith('stackoverflow.com') or
                parsed.netloc.endswith('askubuntu.com') or
                parsed.netloc.endswith('stackexchange.com')
            )
        ):
            # TODO : enable testing for stackoverflow.com on Github Actions
            continue
        else:
            header = None

        req = requests.get(
            url,
            timeout=60,
            headers=header,
        )
        # https://2.python-requests.org/en/master/user/quickstart/#response-status-codes
        req.raise_for_status()


def check_links_in_ipynb(ipynb_file_path:pathlib.Path):
    """
    filename : path to an ipynb file
    """
    check_links_in_ipynb_cells_list(
        nbformat.read(
            ipynb_file_path,
            nbformat.NO_CONVERT,
        )['cells']
    )


def check_links_in_ipynb_cells_list(cells_list):
    """
    cells_list : ipynb notebook's cells

    >>> with open(filename, encoding='utf-8') as ipynb:
        nb = nbformat.read(ipynb, nbformat.NO_CONVERT)
    >>> check_links_in_ipynb_cells_list(nb['cells'])
    """

    just_tested = []

    # cell loop
    for cell in filter(is_cell_markdown, cells_list):
        # see if the cell has links
        # https://stackoverflow.com/questions/16778435/python-check-if-website-exists

        # check simple urls
        check_link_in_cell(cell, get_re_markdown_simple_link(), just_tested)
        # check urls linked to 
        check_link_in_cell(cell, get_re_markdown_image_link(), just_tested)


@functools.lru_cache()
def get_header() -> Dict[str, str]:
    # How to use Python requests to fake a browser visit a.k.a and generate User Agent,
    # https://stackoverflow.com/a/27652558
    return {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/17.1.2 Safari/605.1.15"
        )
    }
