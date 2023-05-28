import pathlib
import sys
import unittest
import urllib.parse as up

import nbformat


acb_folder = pathlib.Path(__file__).parent.parent.absolute()
assert acb_folder.exists(), acb_folder
assert acb_folder.is_dir()
assert (acb_folder / "add_colab_main_buttons.py").exists(), acb_folder


sys.path.insert(0,
    str(acb_folder)
)


import add_colab_main_buttons as acb


class TestAddColabMainButtons(unittest.TestCase):
    def setUp(self) -> None:
        self.without_button_filename = "test_add_colab_main_buttons_without_button.ipynb"

        self.without_button_folder = pathlib.Path(__file__).parent.absolute()
        assert self.without_button_folder.exists(), self.without_button_folder
        assert self.without_button_folder.is_dir()

        self.without_button_full_path = self.without_button_folder / self.without_button_filename
        assert self.without_button_full_path.exists(), self.without_button_full_path
        assert self.without_button_full_path.is_file()

        self.with_button_filename = "test_add_colab_main_buttons_with_button.ipynb"
        self.with_button_folder = pathlib.Path(__file__).parent.absolute()
        assert self.with_button_folder.exists(), self.with_button_folder
        assert self.with_button_folder.is_dir()

        self.with_button_full_path = self.with_button_folder / self.with_button_filename
        assert self.with_button_full_path.exists(), self.with_button_full_path
        assert self.with_button_full_path.is_file()

        self.button_cell = nbformat.read(self.with_button_full_path, nbformat.NO_CONVERT)["cells"][0]
        self.second_code_cell = nbformat.read(self.without_button_full_path, nbformat.NO_CONVERT)["cells"][-1]

    def test__self_button_cell__markdown(self):
        self.assertEqual(self.button_cell["cell_type"], "markdown")

    def test__self_second_code_cell__code(self):
        self.assertEqual(self.button_cell["cell_type"], "markdown")
        self.assertEqual(self.second_code_cell["cell_type"], "code")

    def test_temp_files_have_cells(self):
        nb_without = nbformat.read(self.without_button_full_path, nbformat.NO_CONVERT)
        assert "cells" in nb_without

        nb_with = nbformat.read(self.with_button_full_path, nbformat.NO_CONVERT)
        assert "cells" in nb_with

    def test_is_markdown__button_cell(self):
        result = acb.is_markdown(self.button_cell)
        self.assertTrue(result, msg=self.button_cell)

    def test_metadata_correct__button_cell(self):
        result = acb.metadata_correct(self.button_cell)
        self.assertTrue(result, msg=self.button_cell)

    def test_get_proj_root(self):
        result = acb.get_proj_root()
        assert result.exists(), result
        assert result.is_dir()

        assert (result/".gitignore").exists(), result
        assert (result/"Ch02_Strain").exists() or (result/"00_introduction").exists(), result

    def test_get_rel_path(self):
        result = acb.get_rel_path(self.with_button_full_path)
        self.assertEqual(
            acb.get_proj_root() / result,
            self.with_button_full_path
        )

    def test_get_colab_link(self):
        result = acb.get_colab_link(self.with_button_full_path)

        parsed = up.urlparse(result)
        assert parsed.scheme == "https"
        assert parsed.netloc == "colab.research.google.com"

        path_parts = tuple(parsed.path.split("/"))

        assert path_parts[0] == ""
        assert path_parts[1] == "github"
        assert path_parts[-1] == self.with_button_filename

    def test_get_colab_button_cell(self):
        result = acb.get_colab_button_cell(self.with_button_full_path)
        self.assertEqual({**result, **self.button_cell}, self.button_cell)

    def test_has_button_img__button_cell(self):
        result = acb.has_button_img(self.button_cell)
        self.assertTrue(result)

    def test_has_button_img__code_cell(self):
        result = acb.has_button_img(self.second_code_cell)
        self.assertFalse(result)


class TestAddColabMainButtonsParseArgv(unittest.TestCase):
    def test_parse_argv__no_args(self):
        result = acb.parse_argv([])
        self.assertEqual(result.file, pathlib.Path('None'))
        self.assertEqual(result.directory, acb.get_proj_root())

    def test_parse_argv__one_file_arg(self):
        filename = "test.ipynb"
        result = acb.parse_argv(['dummy.py', "-f", "test.ipynb"])
        self.assertEqual(result.file, pathlib.Path(filename))

    def test_parse_argv__one_dir_arg(self):
        dirname = "test_folder"
        result = acb.parse_argv(['dummy.py', "-d", dirname])
        self.assertEqual(result.file, pathlib.Path('None'))
        self.assertEqual(result.directory, pathlib.Path(dirname))


if "__main__" == __name__:
    unittest.main()
