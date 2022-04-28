import os
import sys
import unittest


import nbformat


sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), os.pardir
        )
    )
)


import add_colab_main_buttons as acb


class TestAddColabMainButtons(unittest.TestCase):
    def setUp(self) -> None:
        self.without_button_filename = "test_add_colab_main_buttons_without_button.ipynb"
        self.without_button_folder = os.path.abspath(os.path.dirname(__file__))
        self.without_button_full_path = os.path.join(self.without_button_folder, self.without_button_filename)

        self.with_button_filename = "test_add_colab_main_buttons_with_button.ipynb"
        self.with_button_folder = os.path.abspath(os.path.dirname(__file__))
        self.with_button_full_path = os.path.join(self.with_button_folder, self.with_button_filename)

        self.button_cell = nbformat.read(self.with_button_full_path, nbformat.NO_CONVERT)["cells"][0]

        self.second_code_cell = nbformat.read(self.without_button_full_path, nbformat.NO_CONVERT)["cells"][-1]

        return super().setUp()

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
        self.assertIn("Ch02_Strain", os.listdir(result), result)

    def test_get_rel_path(self):
        result = acb.get_rel_path(self.with_button_full_path)
        self.assertEqual(
            os.path.join(acb.get_proj_root(), result),
            self.with_button_full_path
        )

    def test_get_colab_link(self):
        result = acb.get_colab_link(self.with_button_full_path)
        self.assertIn(
            result,
            self.button_cell["source"]
        )

    def test_get_colab_button_cell(self):
        result = acb.get_colab_button_cell(self.with_button_full_path)
        self.assertEqual({**result, **self.button_cell}, self.button_cell)

    def test_has_button_img__button_cell(self):
        result = acb.has_button_img(self.button_cell)
        self.assertTrue(result)

    def test_has_button_img__code_cell(self):
        result = acb.has_button_img(self.second_code_cell)
        self.assertFalse(result)


if "__main__" == __name__:
    unittest.main()
