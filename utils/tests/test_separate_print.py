import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import separate_print as sp


@pytest.fixture
def sample_cell() -> str:
    return (
        'print(\'\'\'3.2.5.2\'\'\')\n'
        'f = sy.Function(\'f\')\n'
        'print("f(x).diff(x, x) + f(x) = %s" % (f(x).diff(x, x) + f(x)))\n'
        'print("sy.dsolve(f(x).diff(x, x) + f(x)) = %s" % sy.dsolve(f(x).diff(x, x) + f(x)))\n'
        '\n'
        'm, c, k, t = sy.symbols(\'m c k t\')\n'
        'x = sy.Function(\'x\')\n'
        'vib_eq = m * x(t).diff(t, t) + c * x(t).diff(t) + k * x(t)\n'
        'result = sy.dsolve(vib_eq)\n'
        'print("sy.dsolve() result")\n'
        'print(result)\n'
        '\n'
        'forced_vib_eq = m * x(t).diff(t, t) + c * x(t).diff(t) + k * x(t) - sy.sin(t)\n'
        'result = sy.dsolve(forced_vib_eq)\n'
        'print("forced vibration result:")\n'
        'print(result)\n'
        '\n'
    )
