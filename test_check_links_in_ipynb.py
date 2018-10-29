import os

import pytest

from . import check_links_in_ipynb as cli


# Find absolute path of the parent folder
# This file assumes the parent folder contains a number of .ipynb files
base_path = os.path.abspath(os.path.join(os.path.split(__file__)[0], os.pardir))

# Prepare a list of ipynb files of the base_path
ipynb_file_list = [filename for filename in os.listdir(base_path) if filename.endswith('.ipynb')]


def test_check_links_in_ipynb():
    cli.check_links_in_ipynb(os.path.join(base_path, '00.ipynb'))

patterns = [
    {
        'text': '* `gdb` is the **GNU debugger** that you can use if you compiled with `gcc` or `g++`.\n[\n[ref0](http://www.yolinux.com/TUTORIALS/GDB-Commands.html)\n, [ref1](https://www.quora.com/What-is-a-good-debugger-for-C++-programming)\n, [ref2](https://en.wikipedia.org/wiki/GNU_Debugger)\n]\n\n',
        'urls': {
            'http://www.yolinux.com/TUTORIALS/GDB-Commands.html',
            'https://www.quora.com/What-is-a-good-debugger-for-C++-programming',
            'https://en.wikipedia.org/wiki/GNU_Debugger',
        }
    },
    {
        'text': '* In case of `clang`, `lldb` would be your choice. \n[\n[ref](https://lldb.llvm.org/lldb-gdb.html)\n]\n',
        'urls': {
            'https://lldb.llvm.org/lldb-gdb.html',
        }
    },
    {
        'text': '[![CppCon 2015: Greg Law " Give me 15 minutes & I\'ll change your view of GDB"](https://i.ytimg.com/vi/PorfLSr3DDI/hqdefault.jpg)](https://www.youtube.com/watch?v=PorfLSr3DDI)\n\n',
        'urls': {
            'https://i.ytimg.com/vi/PorfLSr3DDI/hqdefault.jpg',
        } 
    },
    {
        'text': '* You could use following [command](https://stackoverflow.com/questions/8305866/how-to-analyze-a-programs-core-dump-file-with-gdb) to analyze.<br>\n``` sh\ngdb <executable> -c <core-file>\n```',
        'urls': {
            'https://stackoverflow.com/questions/8305866/how-to-analyze-a-programs-core-dump-file-with-gdb',
        }
    }
]


def test_get_re_markdown_simple_link():
    r = cli.get_re_markdown_simple_link()

    for d in patterns:
        assert d['urls'] == set(r.findall(d['text'])), (
            f"\nexpected: {d['urls']}\n"
            f"found: {set(r.findall(d['text']))}"
        )


if "__main__" == __name__:
    test_check_links_in_ipynb()
    test_get_re_markdown_simple_link()
