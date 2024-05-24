import copy
import json
import pathlib
import pytest
import sys


import nbformat


utils_tests_path = pathlib.Path(__file__).parent.resolve()
utils_path = utils_tests_path.parent.resolve()

sys.path.insert(
    0,
    str(utils_path),
)


import find_in_notebook_files as fnf


@pytest.fixture
def notebook_cells_src_str() -> fnf.NotebookFile:
    return nbformat.from_dict(
        {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": "abc\ndef\n",
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": "a = 1\nb = 2\n",
                }
            ],
        }
    )


@pytest.fixture
def notebook_cells_src_splitlines(notebook_cells_src_str) -> fnf.NotebookFile:
    result = copy.deepcopy(notebook_cells_src_str)
    assert isinstance(result["cells"][0]["source"], str)

    result["cells"][0]["source"] = [
        line+'\n' for line in result["cells"][0]["source"].splitlines()
    ]
    result["cells"][1]["source"] = [
        line+'\n' for line in result["cells"][1]["source"].splitlines()
    ]

    return result


@pytest.fixture
def notebook_file__src_str(notebook_cells_src_str, tmp_path):
    ipynb_file = tmp_path / "test_notebook.ipynb"

    with ipynb_file.open('w', encoding="utf-8") as f:
        json.dump(notebook_cells_src_str, f, indent=1, ensure_ascii=False)

    # reload to make sure
    nb = json.loads(ipynb_file.read_text(encoding='utf-8'))

    assert isinstance(nb["cells"][0]["source"], str)
    assert isinstance(nb["cells"][1]["source"], str)

    yield fnf.NotebookFile(ipynb_file)


def test_split_source_lines(notebook_file__src_str, notebook_cells_src_splitlines):
    nb = notebook_file__src_str
    assert isinstance(nb.nb_node["cells"][0]["source"], str)
    assert isinstance(nb.nb_node["cells"][1]["source"], str)

    # function under test
    nb.split_source_lines()

    assert isinstance(nb.nb_node["cells"][0]["source"], list)
    assert isinstance(nb.nb_node["cells"][1]["source"], list)

    nb_list = notebook_cells_src_splitlines
    assert nb.nb_node["cells"][0]["source"] == nb_list["cells"][0]["source"]
    assert nb.nb_node["cells"][1]["source"] == nb_list["cells"][1]["source"]


def test_write(notebook_file__src_str, notebook_cells_src_splitlines, tmp_path):
    nb = notebook_file__src_str
    assert isinstance(nb.nb_node["cells"][0]["source"], str)
    assert isinstance(nb.nb_node["cells"][1]["source"], str)

    new_ipynb_path = tmp_path / "new.ipynb"

    # function under test
    nb.write(new_ipynb_path)

    with new_ipynb_path.open("rt") as f:
        nb_new = json.load(f)

    assert isinstance(nb_new["cells"][0]["source"], list)
    assert isinstance(nb_new["cells"][1]["source"], list)

    nb_list = notebook_cells_src_splitlines
    assert nb.nb_node["cells"][0]["source"] == nb_list["cells"][0]["source"]
    assert nb.nb_node["cells"][1]["source"] == nb_list["cells"][1]["source"]


if "__main__" == __name__:
    pytest.main([__file__])
