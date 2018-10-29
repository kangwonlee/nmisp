import os

import pytest

from . import check_links_in_ipynb as cli


# Find absolute path of the parent folder
# This file assumes the parent folder contains a number of .ipynb files
base_path = os.path.abspath(os.path.join(os.path.split(__file__)[0], os.pardir))

# Prepare a list of ipynb files of the base_path
ipynb_file_list = [filename for filename in os.listdir(base_path) if filename.endswith('.ipynb')]


def test_check_links_in_ipynb():
    cli.check_links_in_ipynb(os.path.join(base_path, '00.ipynb'))


if "__main__" == __name__:
    test_check_links_in_ipynb()
