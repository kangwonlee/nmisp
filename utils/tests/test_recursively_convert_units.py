import pathlib
import pytest
import sys


sys.path.insert(
    0,
    str(pathlib.Path(__file__).parent.parent.absolute()),
)


import recursively_convert_units as rcu


def test__recursively_convert_units__is_ignore():
    sample_path = pathlib.Path(__file__).parent.absolute() / "sample.ipynb"
    assert rcu.is_ignore(sample_path)
