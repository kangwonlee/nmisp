import math

from typing import List, Tuple, Union
import matrix
import matshow


Scalar = Union[int, float, complex]
Vector = List[Scalar]
Matrix = List[Vector]


def eigenvalue_algorithm(mat_a:Matrix, epsilon:float=1e-9, b_verbose:bool=False, b_plot:bool=False) -> Tuple[Matrix, Matrix]:
    mat_a0, mat_x, n, counter = initialize_jacobi_method(mat_a)

    if b_plot:
      abs_ars, ars, r, s = search_max_off_diagonal(mat_a0, n)
      matshow.matshow(counter, abs_ars, r, s, mat_a0, mat_x)

    #########################
    while True:
        abs_ars, ars, r, s = search_max_off_diagonal(mat_a0, n)

        if abs_ars < epsilon:
            break
        if b_verbose:
            print("ars = %s" % ars)
            print("r, s = (%g, %g)" % (r, s))

        arr, ass, cos, sin = get_givens_rotation_elements(ars, b_verbose, mat_a0, r, s)

        jacobi_rotation(ars, arr, ass, cos, sin, mat_a0, mat_x, n, r, s)

        counter += 1

        if b_verbose:
            print("mat_a%03d" % counter)
            matrix.show_mat(mat_a0)
            print("mat_x%03d" % counter)
            matrix.show_mat(mat_x)

        if b_plot:
            matshow.matshow(counter, abs_ars, r, s, mat_a0, mat_x)

    return mat_a0, mat_x


def initialize_jacobi_method(mat_a:Matrix, b_plot:bool=False) -> Tuple[Matrix, Matrix, int, int]:

    if b_plot:
        matshow.remove_all_figure_files()

    n = len(mat_a)
    mat_a0 = matrix.alloc_mat(n, n)

    for i in range(n):
        for j in range(n):
            mat_a0[i][j] = mat_a[i][j]
    mat_x = matrix.get_identity_matrix(n)

    counter = 0

    return mat_a0, mat_x, n, counter




def jacobi_rotation(
    ars:float, arr:float, ass:float, cos:float, sin:float,
    mat_a0:Matrix, mat_x:Matrix,
    n:int, r:int, s:int,
):
    for k in range(n):
        if k == r:
            pass
        elif k == s:
            pass
        else:
            akr = mat_a0[k][r]
            aks = mat_a0[k][s]
            mat_a0[r][k] = akr * cos + aks * sin
            mat_a0[s][k] = aks * cos - akr * sin

            mat_a0[k][r] = mat_a0[r][k]
            mat_a0[k][s] = mat_a0[s][k]

        xkr = mat_x[k][r]
        xks = mat_x[k][s]
        mat_x[k][r] = xkr * cos + xks * sin
        mat_x[k][s] = xks * cos - xkr * sin
    mat_a0[r][r] = arr * cos * cos + 2.0 * ars * sin * cos + ass * sin * sin
    mat_a0[s][s] = arr * sin * sin - 2.0 * ars * sin * cos + ass * cos * cos
    mat_a0[r][s] = mat_a0[s][r] = 0.0


def get_givens_rotation_elements(ars:float, b_verbose:bool, mat_a0:Matrix, r:int, s:int) -> Tuple[float, float, float, float]:
    arr = mat_a0[r][r]
    ass = mat_a0[s][s]
    theta_rad = calc_theta(ars, arr, ass)
    if b_verbose:
        print("theta = %s (deg)" % (theta_rad * 180 / math.pi))
    cos = math.cos(theta_rad)
    sin = math.sin(theta_rad)
    return arr, ass, cos, sin


def calc_theta(ars:float, arr:float, ass:float) -> float:
    theta_rad = 0.5 * math.atan2((2.0 * ars), (arr - ass))
    return theta_rad


def search_max_off_diagonal(mat_a0:Matrix, n:int) -> Tuple[float, float, int, int]:
    r = 0
    s = 1
    ars = mat_a0[r][s]
    abs_ars = abs(ars)

    for i in range(n - 1):
        for j in range(i + 1, n):
            aij = abs(mat_a0[i][j])
            if aij > abs_ars:
                r = i
                s = j
                abs_ars = aij
                ars = mat_a0[i][j]

    return abs_ars, ars, r, s


