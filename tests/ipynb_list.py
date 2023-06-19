import os
import pathlib

from typing import Set, Tuple


def get_filename_tuple(path='', ext='ipynb') -> Tuple[str]:

    path = pathlib.Path(path).absolute()

    if not path.exists():
        print(f"{path} does not exist.", end=' ')
        path = pathlib.Path(__file__).parent.parent.absolute()
        print(f"Using {path}.")

    return tuple(
        map(
            str,    # pytest param needs str for function name
            filter(
                lambda f_path: not is_ignore(f_path.parent.relative_to(path)),
                path.glob(f'**/*.{ext}')
            )
        )
    )


def is_ignore(path:pathlib.Path) -> bool:
    return (set(path.parts).intersection(get_ignore_set()))


def get_ignore_set() -> Set[str]:
    ignore_list = ['.ipynb_checkpoints', '.git', '__pycache__', '.pytest_cache', 'tests', 'utils']

    if 'TEST_IPYNB_IGNORE_FOLDER' in os.environ:
        ignore_list += os.environ['TEST_IPYNB_IGNORE_FOLDER'].split(os.pathsep)

    assert all(map(lambda path: isinstance(path, str), ignore_list))

    return set(ignore_list)
