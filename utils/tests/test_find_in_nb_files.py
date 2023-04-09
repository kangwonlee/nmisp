import copy
import json
import pathlib
import pytest
import sys
import tempfile

import nbformat


sys.path.insert(
    0,
    str(pathlib.Path(__file__).parent.parent.absolute()),
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
def notebook_file__src_str(notebook_cells_src_str) -> fnf.NotebookFile:
    with tempfile.NamedTemporaryFile(mode="w+t", suffix=".ipynb", encoding="utf-8", delete=False) as f:
        json.dump(notebook_cells_src_str, f, indent=1, ensure_ascii=False)
        f.seek(0)

        nb = json.load(f)

    assert isinstance(nb["cells"][0]["source"], str)
    assert isinstance(nb["cells"][1]["source"], str)

    yield fnf.NotebookFile(f.name)

    nb_path = pathlib.Path(f.name)
    if nb_path.exists():
        nb_path.unlink()


def test_splitline_src(notebook_file__src_str, notebook_cells_src_splitlines):
    nb = notebook_file__src_str
    assert isinstance(nb.nb_node["cells"][0]["source"], str)
    assert isinstance(nb.nb_node["cells"][1]["source"], str)

    # function under test
    nb.splitline_src()

    assert isinstance(nb.nb_node["cells"][0]["source"], list)
    assert isinstance(nb.nb_node["cells"][1]["source"], list)

    nb_list = notebook_cells_src_splitlines
    assert nb.nb_node["cells"][0]["source"] == nb_list["cells"][0]["source"]
    assert nb.nb_node["cells"][1]["source"] == nb_list["cells"][1]["source"]


def test_write(notebook_file__src_str, notebook_cells_src_splitlines):
    nb = notebook_file__src_str
    assert isinstance(nb.nb_node["cells"][0]["source"], str)
    assert isinstance(nb.nb_node["cells"][1]["source"], str)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_dir_path = pathlib.Path(tmpdir)

        new_ipynb_path = tmp_dir_path / "new.ipynb"

        # function under test
        nb.write(new_ipynb_path)

        with new_ipynb_path.open("rt") as f:
            nb_new = json.load(f)

        assert isinstance(nb_new["cells"][0]["source"], list)
        assert isinstance(nb_new["cells"][1]["source"], list)

        nb_list = notebook_cells_src_splitlines
        assert nb.nb_node["cells"][0]["source"] == nb_list["cells"][0]["source"]
        assert nb.nb_node["cells"][1]["source"] == nb_list["cells"][1]["source"]
