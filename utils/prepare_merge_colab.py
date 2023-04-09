import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import nb_file_util as nb


def main(argv=sys.argv):
    if 2 <= len(argv):
        path = argv[1]
    else:
        path = nb.get_upper_folder()

    for root, filename in nb.one_level_ipynb_path_file(path):
        full_path = os.path.join(root, filename)
        nodes = nb.read_nodes_from_ipynb(full_path)

        nb.remove_cell_id_from_nodes(nodes)

        if "colab" in nodes["metadata"]:
            del nodes["metadata"]["colab"]

        nb.write_nodes_to_ipynb(full_path, nodes)


if "__main__" == __name__:
    main(sys.argv)
