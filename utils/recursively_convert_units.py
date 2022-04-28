import nbutils.symbol_converter as sc
import os

ignore_path_list = {'__pycache__', '.ipynb_checkpoints', '.git', '.cache', '.idea', 
                    'nbutils', 'tests'}


def is_ignore(path):
    result = False
    path_split_set = set(path.split(os.sep))
    for ignore in ignore_path_list:
        if ignore in path_split_set:
            result= True
            break

    return result


def os_walk_if_not_ignore(root):
    """
    Run an os.walk() loop and yield if not is_ignore()

    root : a path string to a folder
    """
    for root_name, dir_list, filename_list in os.walk(root):
        if not is_ignore(root_name):
            yield root_name, dir_list, filename_list


def is_ipynb(path):
    return '.ipynb' == os.path.splitext(path)[-1]


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


def get_proj_root() -> str:
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir
        )
    )


def iter_ipynb(root:str=get_proj_root()):
    for root_name, _, filename_list in os_walk_if_not_ignore(root):
        # ipynb file loop
        for ipynb_filename in filter(is_ipynb, filename_list):
            full_path = os.path.join(root_name, ipynb_filename)
            yield full_path


def main():

    # file processor
    fp = sc.IpynbUnitConverter(None)

    # Chapter loop
    for full_path in iter_ipynb(os.pardir):
        fp.process_nb_file(full_path, b_write_file=True)


if __name__ == '__main__':
    main()
