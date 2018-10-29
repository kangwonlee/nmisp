import os
import urllib

import pytest
import requests

from . import check_links_in_ipynb as cli


# Find absolute path of the parent folder
# This file assumes the parent folder contains a number of .ipynb files
base_path = os.path.abspath(os.path.join(os.path.split(__file__)[0], os.pardir))

# Prepare a list of ipynb files of the base_path
ipynb_file_list = [filename for filename in os.listdir(base_path) if filename.endswith('.ipynb')]


def test_check_links_in_ipynb_cells_list():
    # still working on
    cli.check_links_in_ipynb_cells_list(sample_ipynb['cells'])


# patterns to test simple urls
# including urls of images
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
    },
    {
        'text':  '* Following code block is an [example](https://stackoverflow.com/questions/35656604/running-cython-in-jupyter-ipython) of the cython code.' ,
        'urls': {
            'https://stackoverflow.com/questions/35656604/running-cython-in-jupyter-ipython',
        }
    },
    {
        'text':  '* Here `%%cython` command is doing all the [plumbing](http://blog.yclin.me/gsoc/2016/07/23/Cython-IPython/) for us.\n* Under the hood, [more](https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html) is going on as we may see later.' ,
        'urls': {
            'http://blog.yclin.me/gsoc/2016/07/23/Cython-IPython/',
            'https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html',
        }
    },
    {
        'text':  ('* Cython can call C/C++ functions as follows.\n'
                '[[ref0](https://cython.readthedocs.io/en/latest/src/userguide/external_C_code.html)]\n'
                ', [[ref1](https://stackoverflow.com/questions/37426534/how-can-i-import-an-external-c-function-into-an-ipython-notebook-using-cython)]\n'
                ', [[ref2](https://stackoverflow.com/questions/19260253/cython-compiling-error-multiple-definition-of-functions)]\n'
                ', [[ref3](https://media.readthedocs.org/pdf/cython/stable/cython.pdf)]\n'
                ', [[ref4](http://www.scipy-lectures.org/advanced/interfacing_with_c/interfacing_with_c.html)]\n'
                ' \n'
                ' '
        ) ,
        'urls': {
            'https://cython.readthedocs.io/en/latest/src/userguide/external_C_code.html',
            'https://stackoverflow.com/questions/37426534/how-can-i-import-an-external-c-function-into-an-ipython-notebook-using-cython',
            'https://stackoverflow.com/questions/19260253/cython-compiling-error-multiple-definition-of-functions',
            'https://media.readthedocs.org/pdf/cython/stable/cython.pdf',
            'http://www.scipy-lectures.org/advanced/interfacing_with_c/interfacing_with_c.html',
        }
    },
    {
        'text':  '* Nowadays in late 2010s, there is an open source project of [**python-control**](https://github.com/python-control/).' ,
        'urls': {
            'https://github.com/python-control/',
        }
    },
    {
        'text':  '* One of the challenges is a numerical library named [**Slycot**](https://github.com/python-control/Slycot) mostly in Fortran.' ,
        'urls': {
            'https://github.com/python-control/Slycot',
        }
    },
    {
        'text':  '* Please refer to [**python-control**](https://github.com/python-control/python-control) and [**Slycot**](https://github.com/python-control/Slycot) for more information.' ,
        'urls': {
            'https://github.com/python-control/python-control',
            'https://github.com/python-control/Slycot',
        }
    },
]


def test_get_re_markdown_simple_link():
    # get regular expression under test
    r = cli.get_re_markdown_simple_link()

    # pattern loop
    for d in patterns:
        # see if found pattens are all correct
        assert d['urls'] == set(r.findall(d['text'])), (
            # assert message
            f"\nexpected: {d['urls']}\n"
            f"found: {set(r.findall(d['text']))}"
        )


# patterns to test urls linked to images
# not including urls of images
patterns_image = [
    {
        'text': '[![CppCon 2015: Greg Law " Give me 15 minutes & I\'ll change your view of GDB"](https://i.ytimg.com/vi/PorfLSr3DDI/hqdefault.jpg)](https://www.youtube.com/watch?v=PorfLSr3DDI)\n\n',
        'urls': {
            'https://www.youtube.com/watch?v=PorfLSr3DDI',
        } 
    },
]


def test_get_re_markdown_image_link():
    # get regular expression under test
    r = cli.get_re_markdown_image_link()

    # pattern loop
    for d in patterns_image:
        # see if found pattens are all correct
        assert d['urls'] == set(r.findall(d['text'])), (
            # assert message
            f"\nexpected: {d['urls']}\n"
            f"found: {set(r.findall(d['text']))}"
        )


# raw ipynb file
# need to join source into a single string
sample_ipynb = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Introducing `gdb`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "* `gdb` is the **GNU debugger** that you can use if you compiled with `gcc` or `g++`.\n",
    "[\n",
    "[ref0](http://www.yolinux.com/TUTORIALS/GDB-Commands.html)\n",
    ", [ref1](https://www.quora.com/What-is-a-good-debugger-for-C++-programming)\n",
    ", [ref2](https://en.wikipedia.org/wiki/GNU_Debugger)\n",
    "]\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "* In case of `clang`, `lldb` would be your choice. \n",
    "[\n",
    "[ref](https://lldb.llvm.org/lldb-gdb.html)\n",
    "]\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Basic use"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "* To use `gdb`, please add `-g` option to comile.  "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "* For example, to build the executable file for `test.c` source file including debug information, following command can be one possible option.\n",
    "\n",
    "``` sh\n",
    "g++ -Wall -g test.c -o a.out\n",
    "gdb a.out\n",
    "```\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "* Please see following table for several gdb commands:"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "| command | expected behavior | example |\n",
    "|:-------:|:-------:|:-------:|\n",
    "| `help` | Show help | `help`<br>`help running` |\n",
    "| `quit` | Exit `gdb` | `quit`<br>`q` |\n",
    "| `apropos <word>` | Search for word in help | `apropos python` |\n",
    "| `info args` | List program commandline arguments | `info args`<br>`i args` |\n",
    "| `info breakpoints` | List breakpoints | `info breakpoints`<br>`i breakpoints` |\n",
    "| `start` | Start the executable and stop at the first line | `start` |\n",
    "| `break <location>` | Set a breakpoint at the location | `break main`<br>`b main`<br>`break 17`<br>`break Matrix::add` |\n",
    "| `run` | Start program execution | `run`<br>`r`<br>`run a.out a b c`<br>`run output.txt`<br>`run input.txt output.txt` |\n",
    "| `break +<n>`<br>`break -<n>` | Set a breakpoint at n lines after or before | `break +1`<br>`break -1` |\n",
    "| `break *<address>` | Set a breakpoint at an instruction address | `break *0x555555554f77` |\n",
    "| `step` | Step *into* next line(s) of code | `step`<br>`s`<br>`s 3` |\n",
    "| `next` | Step *over* next line(s) of code | `next`<br>`n`<br>`n 3` |\n",
    "| `stepi`<br>`si`<br>`nexti`<br>`ni` | `step` and `next` for assembly instruction level | `stepi`<br>`si`<br>`nexti`<br>`ni`<br>... |\n",
    "| `continue` | Continue running the program until the next breakpoint | `continue`<br>`c` |\n",
    "| `continue <n>` | Continue running the program ignoring current breakpoint *n* times | `continue 19`<br>`c 200` |\n",
    "| `finish` | Continue to the end of function | `finish` |\n",
    "| `until <location>` | Continue to the *location* | `until 17`<br>`until add`<br>`until 0x555555554f77` |\n",
    "| `where` | Line number and function name | `where` |\n",
    "| `print <memory>` | Print content of the *memory* | `print argn`<br>`p argn`<br>`p/x argv`<br>`p/d argv` |\n",
    "| `x <address>` | Check the content of the memory at a location | `x/4dw 0x555555554f77` |\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## More idea"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "* Following video presents some more idea on using `gdb`.\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "[![CppCon 2015: Greg Law \" Give me 15 minutes & I'll change your view of GDB\"](https://i.ytimg.com/vi/PorfLSr3DDI/hqdefault.jpg)](https://www.youtube.com/watch?v=PorfLSr3DDI)\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "| command | expected behavior | example |\n",
    "|:-------:|:-------:|:-------:|\n",
    "| `gdb --tui` | Start `gdb` in *Text User Interface* mode | `gdb a.out --tui` |\n",
    "| <kbd>X</kbd>+<kbd>A</kbd> | Start *Text User Interface* mode | <kbd>X</kbd>+<kbd>A</kbd> |\n",
    "| <kbd>L</kbd> | Refresh screen | <kbd>L</kbd> |\n",
    "| <kbd>X</kbd>+<kbd>2</kbd> | Add another window<br>or toggle through display options | <kbd>X</kbd>+<kbd>2</kbd> |\n",
    "| `tui reg general` | Show general purpose registers | `tui reg general` |\n",
    "| <kbd>Ctrl</kbd>+<kbd>P</kbd>/<kbd>N</kbd> | Scroll command window upward/downward | <kbd>Ctrl</kbd>+<kbd>P</kbd>/<kbd>N</kbd> |\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "| command | expected behavior | example |\n",
    "|:-------:|:-------:|:-------:|\n",
    "| `python` | Start built-in python interpreter | `python`<br>`python print('Hi')` |\n",
    "| `python print(gdb.breakpoints())` | Show breakpoints | `python print(gdb.breakpoints())` |\n",
    "| `python gdb.Breakpoints(<location>)` | Create a breakpoint | `python gdb.Breakpoints('7')` |\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "| command | expected behavior | example |\n",
    "|:-------:|:-------:|:-------:|\n",
    "| `reverse-stepi` | Backstep assembly instruction | `reverse-stepi` |\n",
    "| `reverse-continue` | Backward continue until a breakpoint | `reverse-continue` |\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## When *core* was dumped"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "* Sometimes your C/C++ program would crash and the *core* might have been *dump*ed."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "* You could use following [command](https://stackoverflow.com/questions/8305866/how-to-analyze-a-programs-core-dump-file-with-gdb) to analyze.<br>\n",
    "``` sh\n",
    "gdb <executable> -c <core-file>\n",
    "```"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

# joining the source code parts of the raw ipynb
for i in range(len(sample_ipynb['cells'])):
    sample_ipynb['cells'][i]['source'] = ''.join(sample_ipynb['cells'][i]['source'])


def test_check_link_in_cell():
    # This case is supposed to success
    google_cell =  {
    "cell_type": "markdown",
    "metadata": {},
    "source": ''.join([
        "[ref0](http://www.google.com)\n",
        "\n"
    ])
    }

    # This case is supposed to fail
    fail_cell =  {
    "cell_type": "markdown",
    "metadata": {},
    "source": ''.join([
        "[ref0](https://en.wikipedia.org/wiki/New_and_delete_&#40;C%2B%2B&#41;)\n",
        "\n"
    ])
    }    

    r = cli.get_re_markdown_simple_link()
    
    # function under test
    # success case
    cli.check_link_in_cell(google_cell, r)

    try:
        # function under test
        # failure case
        cli.check_link_in_cell(fail_cell, r)
    except urllib.error.URLError as e:
        # present expected error
        print(e)
        pass
    except requests.exceptions.ConnectionError as e:
        # present expected error
        print(e)
        pass
    except BaseException as e:
        # just in case
        print(e)
    else:
        # expected exception not raised
        raise NotImplementedError
