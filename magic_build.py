# https://stackoverflow.com/questions/10361206/how-to-run-an-ipython-magic-from-a-script-or-timing-a-python-script
import IPython


try:
    ipython = IPython.get_ipython()
except AttributeError:
    try:
        import IPython.core.ipapi
        ipython = IPython.core.ipapi.get()
    except ModuleNotFoundError:
        import IPython.ipapi
        ipython = IPython.ipapi.get()


def write_file(filename, code):
    ipython.run_cell_magic("writefile", filename, code)

