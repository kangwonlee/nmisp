from typing import List, Tuple, Union

Scalar = Union[int, float, complex]
Vector = List[Scalar]
Matrix = List[Vector]


def alloc_vec(n:int) -> Vector:
    return [0.0] * n


def alloc_mat(m:int, n:int) -> Matrix:
    result = alloc_vec(m)
    for k in range(m):
        result[k] = alloc_vec(n)
    return result


def get_identity_matrix(m_row):
    mat_i = alloc_mat(m_row, m_row)
    for i_pivot in range(m_row):
        mat_i[i_pivot][i_pivot] = 1.0
    return mat_i
