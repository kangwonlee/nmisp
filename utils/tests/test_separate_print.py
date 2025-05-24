import os
import sys

import nbformat
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


@pytest.fixture
def sample_seperation_dict() -> dict:
    return {
        'print("a = %s" % a)' : 'a',
        'print("sy.pi**2 = %s" % sy.pi ** 2)' : 'sy.pi ** 2',
        'print("sy.pi.evalf() = %s" % sy.pi.evalf())' : 'sy.pi.evalf()',
        'print("sy.pi + sy.exp(1) = %s" % (sy.pi + sy.exp(1)))' : '(sy.pi + sy.exp(1))',
        'print("(sy.pi + sy.exp(1)).evalf() = %s" % ((sy.pi + sy.exp(1)).evalf()))' : '((sy.pi + sy.exp(1)).evalf())',
        'print("sy.oo = %s" % sy.oo)' : 'sy.oo',
        'print("sy.oo > 99999 = %s" % (sy.oo > 99999))' : '(sy.oo > 99999)',
        'print("sy.sqrt(2) = %s" % (sy.sqrt(2).evalf(100)))' : '(sy.sqrt(2).evalf(100))',
        'print("1/2 + 1/3 = %s" % (sy.Rational(1, 2) + sy.Rational(1, 3)))' : '(sy.Rational(1, 2) + sy.Rational(1, 3))',
        'print("solution = %s" % sy.simplify(solution))' : 'sy.simplify(solution)',
        'print("x+y+x-y = %s" % (x + y + x - y))' : '(x + y + x - y)',
        'print("(x+y)**2 = %s" % ((x + y) ** 2))' : '((x + y) ** 2)',
        'print("sy.expand((x+y)**3) = %s" % sy.expand((x + y) ** 3))' : 'sy.expand((x + y) ** 3)',
        'print("sy.expand(x+y, complex=True) = %s" % sy.expand(x + y, complex=True))' : 'sy.expand(x + y, complex=True)',
        'print("sy.expand(sy.cos(x+y), trig=True) = %s" % sy.expand(sy.cos(x + y), trig=True))' : 'sy.expand(sy.cos(x + y), trig=True)',
        'print("sy.simplify((x+x*y)/x) = %s" % sy.simplify((x + x * y) / x))' : 'sy.simplify((x + x * y) / x)',
        'print("sy.limit(sy.sin(x)/x,x,0) = %s" % sy.limit(sy.sin(x) / x, x, 0))' : 'sy.limit(sy.sin(x) / x, x, 0)',
        'print("sy.limit(x,x,sy.oo) = %s" % sy.limit(x, x, sy.oo))' : 'sy.limit(x, x, sy.oo)',
        'print("sy.limit(1/x,x,sy.oo) = %s" % sy.limit(1 / x, x, sy.oo))' : 'sy.limit(1 / x, x, sy.oo)',
        'print("sy.limit(x**x,x,0) = %s" % sy.limit(x ** x, x, 0))' : 'sy.limit(x ** x, x, 0)',
        'print("sy.diff(sy.sin(x), x) = %s" % sy.diff(sy.sin(x), x))' : 'sy.diff(sy.sin(x), x)',
        'print("sy.diff(sy.sin(2*x), x) = %s" % sy.diff(sy.sin(2 * x), x))' : 'sy.diff(sy.sin(2 * x), x)',
        'print("sy.diff(sy.tan(x), x) = %s" % sy.diff(sy.tan(x), x))' : 'sy.diff(sy.tan(x), x)',
        'print("sy.limit((sy.tan(x+y)-sy.tan(x))/y,y,0) = %s" % sy.limit((sy.tan(x + y) - sy.tan(x)) / y, y, 0))' : 'sy.limit((sy.tan(x + y) - sy.tan(x)) / y, y, 0)',
        'print("sy.diff(sy.sin(2*x), x, 1) = %s" % sy.diff(sy.sin(2 * x), x, 1))' : 'sy.diff(sy.sin(2 * x), x, 1)',
        'print("sy.diff(sy.sin(2*x), x, 2) = %s" % sy.diff(sy.sin(2 * x), x, 2))' : 'sy.diff(sy.sin(2 * x), x, 2)',
        'print("sy.diff(sy.sin(2*x), x, 3) = %s" % sy.diff(sy.sin(2 * x), x, 3))' : 'sy.diff(sy.sin(2 * x), x, 3)',
        'print("sy.series(sy.cos(x), x) = %s" % sy.series(sy.cos(x), x))' : 'sy.series(sy.cos(x), x)',
        'print("sy.series(1/sy.cos(x), x) = %s" % sy.series(1 / sy.cos(x), x))' : 'sy.series(1 / sy.cos(x), x)',
        'print("sy.integrate(6*x**5, x) = %s" % sy.integrate(6 * x ** 5, x))' : 'sy.integrate(6 * x ** 5, x)',
        'print("sy.integrate(sy.sin(x), x) = %s" % sy.integrate(sy.sin(x), x))' : 'sy.integrate(sy.sin(x), x)',
        'print("sy.integrate(sy.log(x), x) = %s" % sy.integrate(sy.log(x), x))' : 'sy.integrate(sy.log(x), x)',
        'print("sy.integrate(2*x + sy.sinh(x), x) = %s" % sy.integrate(2 * x + sy.sinh(x), x))' : 'sy.integrate(2 * x + sy.sinh(x), x)',
        'print("sy.integrate(sy.exp(-x**2)*sy.erf(x), x) = %s" % sy.integrate(sy.exp(-x ** 2) * sy.erf(x), x))' : 'sy.integrate(sy.exp(-x ** 2) * sy.erf(x), x)',
        'print("sy.integrate(x**3, (x, -1, 1)) = %s" % sy.integrate(x ** 3, (x, -1, 1)))' : 'sy.integrate(x ** 3, (x, -1, 1))',
        'print("sy.integrate(sy.sin(x), (x, 0, sy.pi/2)) = %s" % sy.integrate(sy.sin(x), (x, 0, sy.pi / 2)))' : 'sy.integrate(sy.sin(x), (x, 0, sy.pi / 2))',
        'print("sy.integrate(sy.cos(x), (x, -sy.pi/2, sy.pi/2)) = %s" % sy.integrate(sy.cos(x), (x, -sy.pi / 2, sy.pi / 2)))' : 'sy.integrate(sy.cos(x), (x, -sy.pi / 2, sy.pi / 2))',
        'print("sy.integrate(sy.exp(-x), (x, 0, sy.oo)) = %s" % sy.integrate(sy.exp(-x), (x, 0, sy.oo)))' : 'sy.integrate(sy.exp(-x), (x, 0, sy.oo))',
        'print("sy.integrate(sy.exp(-x**2), (x, -sy.oo, sy.oo)) = %s" % sy.integrate(sy.exp(-x ** 2), (x, -sy.oo, sy.oo)))' : 'sy.integrate(sy.exp(-x ** 2), (x, -sy.oo, sy.oo))',
        'print("sy.solve(x**4 - 1, x) = %s" % sy.solve(x ** 4 - 1, x))' : 'sy.solve(x ** 4 - 1, x)',
        'print("sy.solve([x + 5*y - 2, -3*x + 6*y - 15], [x,y]) = %s" % sy.solve([x + 5 * y - 2, -3 * x + 6 * y - 15], [x, y]))' : 'sy.solve([x + 5 * y - 2, -3 * x + 6 * y - 15], [x, y])',
        'print("sy.solve(sy.exp(x) + 1, x) = %s" % sy.solve(sy.exp(x) + 1, x))' : 'sy.solve(sy.exp(x) + 1, x)',
        'print("sy.factor(f) = %s" % sy.factor(f))' : 'sy.factor(f)',
        'print("sy.factor(f, modulus=5) = %s" % sy.factor(f, modulus=5))' : 'sy.factor(f, modulus=5)',
        'print("sy.satisfiable(x&y) = %s" % sy.satisfiable(x & y))' : 'sy.satisfiable(x & y)',
        'print("sy.satisfiable(x^y) = %s" % sy.satisfiable(x ^ y))' : 'sy.satisfiable(x ^ y)',
        'print("sy.Matrix([[1,0], [0,1]]) = %s" % sy.Matrix([[1, 0], [0, 1]]))' : 'sy.Matrix([[1, 0], [0, 1]])',
        'print("A = %s" % A)' : 'A',
        'print("A**2 = %s" % A ** 2)' : 'A ** 2',
        'print("f(x).diff(x, x) + f(x) = %s" % (f(x).diff(x, x) + f(x)))' : '(f(x).diff(x, x) + f(x))',
        'print("sy.dsolve(f(x).diff(x, x) + f(x)) = %s" % sy.dsolve(f(x).diff(x, x) + f(x)))' : 'sy.dsolve(f(x).diff(x, x) + f(x))',
    }


def test_strip_parentheses_single():
    input_str = '("sy.pi**2 = %s" % sy.pi ** 2)'
    expected = input_str[1:-1]

    result = sp.strip_parentheses(input_str)

    assert result == expected


def test_strip_parentheses_double():
    input_str = '("sy.satisfiable(x&y) = %s" % sy.satisfiable(x & y))'
    expected = input_str[1:-1]

    result = sp.strip_parentheses(input_str)

    assert result == expected


def test_is_line_to_separate(sample_cell):
    separate_list = [
        False,
        False,
        True,
        True,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    ]

    for input_str, expected in zip(sample_cell.splitlines(), separate_list):
        assert sp.is_line_to_separate(input_str) == expected


def test_separate_line(sample_seperation_dict):
    for input_str, expected in sample_seperation_dict.items():
        assert sp.separate_line(input_str) == expected, (input_str, expected)


def test_flush_source_lines_empty():
    result_list = []
    input_list = []

    sp.flush_source_lines(input_list, result_list)

    assert not result_list


def test_flush_source_lines_one_line():
    line_0 = 'print("Hello Python")'
    result_list = []
    input_list = [line_0]

    assert not result_list

    sp.flush_source_lines(input_list, result_list)

    assert result_list
    assert 'code' == result_list[0]['cell_type']
    assert line_0 in result_list[0]['source']


def test_get_new_code_cell():
    line_0 = 'print("Hello Python")'
    input_list = [line_0]

    result = sp.get_new_code_cell(input_list)

    assert 'code' == result['cell_type']
    assert line_0 in result['source']


def test_process_cell():

    lines_dict = [
        {'cell': 0, 'line':"""print('''3.2.1.3''')"""},
        {'cell':-1, 'line':""""""},
        {'cell': 0, 'line':"""x = sy.Symbol('x')"""},
        {'cell': 0, 'line':"""y = sy.Symbol('y')"""},
        {'cell':-1, 'line':""""""},
        {'cell': 0, 'line':"""print("x+y+x-y = %s" % (x + y + x - y))""", 'expected': "x + y + x - y"},
        {'cell':-1, 'line':""""""},
        {'cell': 1, 'line':"""print("(x+y)**2 = %s" % (x + y) ** 2)""", 'expected': "(x + y) ** 2"},
    ]

    input_cell = nbformat.v4.new_code_cell(source='\n'.join(
        [d['line'] for d in lines_dict]
    ))

    result_list = sp.process_cell(input_cell)

    for line_dict in lines_dict:

        expected = line_dict.get('expected', line_dict['line'])

        if 0 <= line_dict['cell']:
            for k, result_cell in enumerate(result_list):
                if k == line_dict['cell']:
                    assert expected in result_cell.source
                else:
                    assert expected not in result_cell.source


def test_process_cell_interchanging():

    lines_dict = [
        {'cell': 0, 'line':"""print('''3.2.1.2''')"""},
        {'cell': 0, 'line':"""print("sy.sqrt(2) = %s" % sy.sqrt(2).evalf(100))"""                 , 'expected': "sy.sqrt(2).evalf(100)"},
        {'cell':-1, 'line':""""""},
        {'cell': 1, 'line':"""print("1/2 + 1/3 = %s" % (sy.Rational(1, 2) + sy.Rational(1, 3)))""", 'expected': "(sy.Rational(1, 2) + sy.Rational(1, 3))"},
        {'cell':-1, 'line':""""""},
        {'cell': 2, 'line':"""F, r, sigma_max, sf = sy.symbols('F r sigma_max safety_factor')"""},
        {'cell':-1, 'line':""""""},
        {'cell': 2, 'line':"""area = sy.pi * r * r"""},
        {'cell': 2, 'line':"""sigma = F / area"""},
        {'cell': 2, 'line':"""solution = sy.solve([sigma - sigma_max / sf], r)"""},
        {'cell': 2, 'line':"""print("solution = %s" % sy.simplify(solution))"""                   , 'expected': "sy.simplify(solution)"},
    ]
    input_cell = nbformat.v4.new_code_cell(source='\n'.join(
        [d['line'] for d in lines_dict]
    ))

    result_list = sp.process_cell(input_cell)

    for line_dict in lines_dict:

        expected = line_dict.get('expected', line_dict['line'])

        if 0 <= line_dict['cell']:
            for k, result_cell in enumerate(result_list):
                if k == line_dict['cell']:
                    assert expected in result_cell.source
                else:
                    assert expected not in result_cell.source


def test_process_cell__markdown():

    line_0 = '# `sympy`\n'

    input_cell = nbformat.v4.new_markdown_cell(source=line_0)

    result_list = sp.process_cell(input_cell)

    assert line_0 in result_list[0].source

    assert 1 == len(result_list), len(result_list)


if "__main__" == __name__:
    pytest.main()
