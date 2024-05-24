import copy
import json
import pathlib
import sys
from typing import Any, Dict, List

import nbformat
import pytest


utils_tests_path = pathlib.Path(__file__).parent.resolve()
utils_path = utils_tests_path.parent.resolve()

sys.path.insert(
    0,
    str(utils_path),
)


import find_in_notebook_files as fnf


CELL = Dict[str, Any]
NOTEBOOK = Dict[str, List[CELL]]


@pytest.fixture
def base_notebook_data() -> NOTEBOOK:
    """Fixture providing base notebook data as a dictionary."""
    return {
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


@pytest.fixture
def notebook_file(
        base_notebook_data:NOTEBOOK,
        tmp_path:pathlib.Path) -> fnf.NotebookFile:
    """Fixture creating a temporary notebook file from base data."""
    ipynb_file = tmp_path / "test_notebook.ipynb"
    with ipynb_file.open("w", encoding="utf-8") as f:
        json.dump(base_notebook_data, f, indent=1, ensure_ascii=False)

    return fnf.NotebookFile(ipynb_file)


@pytest.fixture
def notebook_file_with_ids(
        base_notebook_data:NOTEBOOK,
        tmp_path:pathlib.Path) -> fnf.NotebookFile:  # Added type hint
    """Fixture creating a temporary notebook file with cell IDs."""
    ipynb_file = tmp_path / "test_notebook_with_ids.ipynb"

    nb_data_with_ids = copy.deepcopy(base_notebook_data)
    for i, cell in enumerate(nb_data_with_ids["cells"]):
        cell.update({"id": f"cell-{i}", "metadata": {"id": f"metadata-cell-{i}"}})

    with ipynb_file.open("w", encoding="utf-8") as f:
        nbformat.write(nb_data_with_ids, f)  # Use json.dump here
        
    return fnf.NotebookFile(ipynb_file)


def test_split_source_lines(notebook_file:fnf.NotebookFile):
    """Test splitting cell source code into individual lines."""
    nb = notebook_file
    original_sources = [cell.source for cell in nb.nb_node.cells]

    # function under test
    nb.split_source_lines()

    for i, cell in enumerate(nb.nb_node.cells):
        assert isinstance(cell.source, list)
        assert cell.source == original_sources[i].splitlines(keepends=True)


def test_write(notebook_file:fnf.NotebookFile, tmp_path):
    """Test writing the modified notebook to a new file."""
    nb = notebook_file
    nb.split_source_lines()

    new_ipynb_path = tmp_path / "new.ipynb"
    # function under test
    nb.write(new_ipynb_path)

    with new_ipynb_path.open("r", encoding="utf-8") as f:
        nb_new = nbformat.read(f, nbformat.NO_CONVERT)

    # Compare cell sources from the original and written notebooks
    for original_cell, new_cell in zip(notebook_file.nb_node.cells, nb_new.cells):
        assert original_cell.source == new_cell.source


def test_remove_cell_id_from_nodes(notebook_file_with_ids:fnf.NotebookFile):
    """Test removing cell IDs from the notebook."""
    nb = notebook_file_with_ids
    assert any("id" in cell or "id" in cell.get("metadata", {}) for cell in nb.nb_node.cells)  

    # function under test
    modified = nb.remove_cell_id_from_nodes()
    assert modified  # Check if any IDs were removed
    assert not any("id" in cell or "id" in cell.get("metadata", {}) for cell in nb.nb_node.cells)


if "__main__" == __name__:
    pytest.main([__file__])
