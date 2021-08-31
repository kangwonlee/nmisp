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


def mul_mat(mat_a, mat_b):
    m_row_a, n_col_a = shape(mat_a)
    m_row_b, n_col_b = shape(mat_b)
    mat_c = alloc_mat(m_row_a, n_col_b)
    for i in range(m_row_a):
        for j in range(n_col_b):
            mat_c[i][j] = 0.0
            for k in range(n_col_a):
                # Multiply and ACcumulation MAC Operation
                mat_c[i][j] += mat_a[i][k] * mat_b[k][j]
    return mat_c


def shape(mat_a):
    assert all(map(lambda row:len(row) == len(mat_a[0]), mat_a[1:]))
    return len(mat_a), len(mat_a[0])


def transpose_mat(mat_a):
    _, __ = shape(mat_a)
    return list(zip(*mat_a))
