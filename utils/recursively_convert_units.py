import os
import pathlib


ignore_path_list = {'__pycache__', '.ipynb_checkpoints', '.git', '.cache', '.idea', 
                    'nbutils', 'tests', 'utils', '.github'}


def is_ignore(path:pathlib.Path, ignore_set:set=set(ignore_path_list)) -> bool:
    path_split_set = set(pathlib.Path(path).parts)
    return len(ignore_set.intersection(path_split_set))


def os_walk_if_not_ignore(root):
    """
    Run an os.walk() loop and yield if not is_ignore()

    root : a path string to a folder
    """
    for root_name, dir_list, filename_list in os.walk(root):
        if not is_ignore(root_name):
            yield root_name, dir_list, filename_list


def is_ipynb(path:pathlib.Path) -> bool:
    return '.ipynb' == pathlib.Path(path).suffix


def gen_filename_ipynb(filename_list):
    """
    Generator for ipynb filenames in the filename_list

    filename_list : list of filenames within a folder
    """
    for filename in filename_list:
        if is_ipynb(filename):
            yield filename    


def gen_ipynb(root):
    """
    Generate ipynb files within each chapter
    root(==parent folder of chapter folders) -> chapter_path, ipynb_filename
    """
    # Chapter folder
    for chapter_path, _, filename_list in os_walk_if_not_ignore(root):

        # Notebook file loop
        for ipynb_filename in filter(is_ipynb, filename_list):
            yield chapter_path, ipynb_filename


def get_proj_root() -> pathlib.Path:
    result = pathlib.Path(__file__).parent.parent.absolute()
    assert result.exists(), result
    assert result.is_dir()
    assert (result / ".gitignore").exists(), (result, result.glob("*"))
    return result


def iter_ipynb(root:str=None):

    if root is None:
        root = get_proj_root()

    for root_name, _, filename_list in os_walk_if_not_ignore(root):
        # ipynb file loop
        for ipynb_filename in filter(is_ipynb, filename_list):
            full_path = os.path.join(root_name, ipynb_filename)
            yield full_path
