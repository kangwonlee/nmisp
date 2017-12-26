"""
Jupyter notebook could be good for educational purpose.
Before release in class, output generated during testing and execution number need to be removed.
"""

import os
import sys

import nbformat

import nb_file_util as fu


# Use this module to read or write notebook files as particular nbformat versions.


class CellProcessorDeleteOutput(fu.CellProcessorBase):
    def process_cell(self):
        self.remove_cell_output()


if __name__ == '__main__':

    def main(argv):
        if 1 < len(argv):
            filename = argv[1]
            p = fu.FileProcessor(filename, CellProcessorDeleteOutput())
            p.process_nb_file()
        else:
            print("Usage : python %s <notebook file path>" % os.path.split(__file__)[-1])
            help(nbformat)


    main(sys.argv)
