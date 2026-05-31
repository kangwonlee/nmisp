import os

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

    return ax


def common_max_weight(snapshots:List[Matrix]) -> float:
    '''
    모든 단계에 걸쳐 같은 상자 크기 기준을 쓰기 위한 공통 max_weight<br>
    A single Hinton scale shared across every step, so a box of a given size
    means the same magnitude in every frame and elements can be compared
    across iterations.
    '''
    peak = max(np.abs(np.array(m)).max() for m in snapshots)
    return 2 ** np.ceil(np.log2(peak)) if peak > 0 else 1.0


def hinton_step_slider(
        snapshots:List[Matrix], titles:List[str]=None,
        description:str='step', max_weight:float=None,
    ):
    '''
    반복 단계별 행렬 스냅숏을 ipywidgets 슬라이더로 넘겨보는 Hinton 다이어그램<br>
    Scrub a Hinton diagram across a list of per-iteration matrix snapshots.

    snapshots : list of matrices, one per iteration step.
    titles    : optional per-step title strings.

    All frames share one Hinton scale (see `common_max_weight`) so a box of a
    given size always means the same magnitude — that is what lets a learner
    watch individual elements shrink or grow from step to step.

    Under continuous integration (`CI` env var) there is no widget backend, so
    only the final frame is rendered; the notebook still executes top-to-bottom.
    '''
    from ipywidgets import interact, IntSlider

    n = len(snapshots)
    if max_weight is None:
        max_weight = common_max_weight(snapshots)

    def render(step):
        plt.close()
        fig, ax = plt.subplots()
        hinton(np.array(snapshots[step]), max_weight=max_weight, ax=ax)
        suffix = f" : {titles[step]}" if titles is not None else ''
        ax.set_title(f"step {step}/{n - 1}{suffix}")
        plt.show()

    if os.getenv('CI', False):
        # 위젯 대신 마지막 단계만 렌더 / render only the final step instead of a widget
        render(n - 1)
    else:
        interact(
            render,
            step=IntSlider(min=0, max=n - 1, step=1, value=0, description=description),
        )


def element_trace(
        snapshots:List[Matrix], indices:List[Tuple[int, int]],
        labels:List[str]=None, logy:bool=False, ax=None,
    ):
    '''
    선택한 행렬 원소 a[i][j]가 반복에 따라 어떻게 변하는지 추적하는 꺾은선 그래프<br>
    Trace the numeric value of selected entries a[i][j] across iteration steps.

    The Hinton slider shows *structure*; this shows the *value* of a chosen
    entry converging (e.g. a diagonal entry approaching an eigenvalue).
    '''
    steps = list(range(len(snapshots)))
    arrs = [np.array(m) for m in snapshots]

    ax = ax if ax is not None else plt.gca()
    for k, (i, j) in enumerate(indices):
        ys = [a[i, j] for a in arrs]
        label = labels[k] if labels is not None else f"a[{i}][{j}]"
        ax.plot(steps, ys, marker='o', label=label)

    ax.set_xlabel('iteration step')
    ax.set_ylabel('element value')
    if logy:
        ax.set_yscale('log')
    ax.grid(True)
    ax.legend()

    return ax
