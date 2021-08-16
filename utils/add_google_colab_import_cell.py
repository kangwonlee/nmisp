import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import nb_file_util as nb


def main(argv=sys.argv):
    if 2 <= len(argv):
        path = argv[1]
    else:
        path = nb.get_upper_folder()

    code = "# test code"

    nb.add_code_to_all_ipynb_tree(0, code, path)


if "__main__" == __name__:
    main(sys.argv)
