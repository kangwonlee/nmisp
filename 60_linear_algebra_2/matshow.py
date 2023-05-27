from typing import List, Tuple, Union

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np


Scalar = Union[int, float, complex]
Vector = List[Scalar]
Matrix = List[Vector]


def matshow(counter, abs_ars, r, s, mat_a0, mat_x, ax=None):

    if 3 > len(mat_a0):
        matshow22(counter, abs_ars, r, s, mat_a0, mat_x)
    elif 3 == len(mat_a0):
        matshow33(counter, abs_ars, r, s, mat_a0, mat_x)
    else:
        if ax is None:
            ax = plt.gca()
        else:
            ax.cla()
        hinton(
            np.hstack((
                np.array(mat_a0), np.array(mat_x)
            )),
            ax=ax
        )
        ax.set_title(get_title(counter, abs_ars, r, s))

    plt.savefig(f"iteration_{len(mat_a0):03d}_{counter:03d}.png")
    plt.close()


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


def remove_all_figure_files(ext:str='png') -> None:
  for filename in os.listdir():
    if os.path.splitext(filename)[-1].lower().endswith(ext.lower()):
      os.remove(filename)


def hinton(matrix, max_weight=None, ax=None):
    '''
    Draw Hinton diagram for visualizing a weight matrix.
    https://matplotlib.org/stable/gallery/specialty_plots/hinton_demo.html
    '''
    if ax is None:
      b_ax_none = True
      ax = plt.gca()
    else:
      b_ax_none = False

    if not max_weight:
        max_weight = 2 ** np.ceil(np.log2(np.abs(matrix).max()))

    ax.patch.set_facecolor('gray')
    ax.set_aspect('equal', 'box')

    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())

    for (y, x), w in np.ndenumerate(matrix):
        color = 'white' if w > 0 else 'black'
        size = np.sqrt(abs(w) / max_weight)
        rect = plt.Rectangle([x - size / 2, y - size / 2], size, size,
                             facecolor=color, edgecolor=color)
        ax.add_patch(rect)

    ax.autoscale_view()
    ax.invert_yaxis()

    if b_ax_none:
      plt.show()
      plt.close()
