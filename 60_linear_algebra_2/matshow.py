from typing import List, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np


Scalar = Union[int, float, complex]
Vector = List[Scalar]
Matrix = List[Vector]


def matshow(counter, abs_ars, r, s, mat_a0, mat_x):

  if 3 > len(mat_a0):
    matshow22(counter, abs_ars, r, s, mat_a0, mat_x)
  elif 3 == len(mat_a0):
    matshow33(counter, abs_ars, r, s, mat_a0, mat_x)
  else:
    plt.matshow(
      np.hstack((
        np.array(mat_a0), np.array(mat_x)
      ))
    )
    plt.title(get_title(counter, abs_ars, r, s))

  plt.savefig(f"iteration{counter:03d}.png")


def get_title(counter, abs_ars, r, s) -> str:
  return f"iteration{counter:03d} r={r} s={s} abs(a[{r}][{s}])={abs_ars:g}"


def matshow22(counter, abs_ars, r, s, mat_a0, mat_x):
  fig, axes = plt.subplots(2, 2)

  fig.suptitle(get_title(counter, abs_ars, r, s))
  axes[0][0].matshow(np.array(mat_a0))

  axes[0][1].matshow(np.array(mat_x))

  axes[1][0].plot((0, mat_a0[0][0]), (0, mat_a0[0][1]),)
  axes[1][0].plot((0, mat_a0[1][0]), (0, mat_a0[1][1]),)
  axes[1][0].axis('equal')
  axes[1][0].grid(True)

  axes[1][1].plot((0, mat_x[0][0]), (0, mat_x[0][1]),)
  axes[1][1].plot((0, mat_x[1][0]), (0, mat_x[1][1]),)
  axes[1][1].axis('equal')
  axes[1][1].grid(True)


def matshow33(counter, abs_ars, r, s, mat_a0, mat_x):
  fig = plt.figure()

  axes = (
    (fig.add_subplot(2, 2, 1), fig.add_subplot(2, 2, 2),),
    (
      fig.add_subplot(2, 2, 3, projection='3d'),
      fig.add_subplot(2, 2, 4, projection='3d'),
    )
  )

  fig.suptitle(get_title(counter, abs_ars, r, s))
  axes[0][0].matshow(np.array(mat_a0))

  axes[0][1].matshow(np.array(mat_x))

  axes[1][0].quiver(
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    mat_a0[0],
    mat_a0[1],
    mat_a0[2],
    length=1, normalize=True,
  )
  axes[1][0].grid(True)

  axes[1][1].quiver(
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    mat_x[0],
    mat_x[1],
    mat_x[2],
    length=1, normalize=True,
  )
  axes[1][1].grid(True)
