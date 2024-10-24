import pathlib


ignore_path_list = {
    '__pycache__', '.ipynb_checkpoints', '.git', '.cache', '.idea', 
    'nbutils', 'tests', 'utils', '.github'}


def is_ignore(path:pathlib.Path, ignore_set:set=set(ignore_path_list)) -> bool:
    path_split_set = set(path.parts)
    return len(ignore_set.intersection(path_split_set))


def walk_ipynb(root:pathlib.Path):
    """
    Run an root.rglob() loop and yield if not is_ignore()

    root : a pathlib.Path to a folder
    """
    for p in root.rglob("*"):  # Use rglob to traverse all subdirectories
        if p.is_dir() and not is_ignore(p):  # Check if it's a directory and not ignored
            yield p, list(p.iterdir()), [f.name for f in p.iterdir() if f.is_file()]


def is_ipynb(path:pathlib.Path) -> bool:
    return '.ipynb' == pathlib.Path(path).suffix


def gen_ipynb(root):
    """
    Generate ipynb files within each chapter
    root(==parent folder of chapter folders) -> chapter_path, ipynb_filename
    """
    # Chapter folder
    for chapter_path, _, filename_list in walk_ipynb(root):

        # Notebook file loop
        for ipynb_filename in filter(is_ipynb, filename_list):
            yield chapter_path, ipynb_filename


def get_proj_root() -> pathlib.Path:
    result = pathlib.Path(__file__).parent.parent.absolute()
    assert result.exists(), result
    assert result.is_dir()
    assert (result / ".gitignore").exists(), (result, result.glob("*"))
    return result


def iter_ipynb(root:pathlib.Path=get_proj_root()):
    for root_name, _, filename_list in walk_ipynb(root):
        # ipynb file loop
        for ipynb_filename in filter(is_ipynb, filename_list):
            full_path = root_name / ipynb_filename
            yield full_path
