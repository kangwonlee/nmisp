# %% [markdown]
# <a href="https://colab.research.google.com/github/kangwonlee/nmisp/blob/main/15_optimization/038_Classification_Optimization-Rasterization.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
#

# %% [markdown]
# # 분류 최적화<br>Classification Optimization
#

# %% [markdown]
# * Let's say there are two sets : $set_0$ & $set_1$.<br>두 집합 $set_0$ & $set_1$ 이 있다고 하자.
# * Each set has $\frac{n}{2}$ entries.<br>각 집합에는 각각 $\frac{n}{2}$ 원소가 있다.
# * We can measure two variables : $\textbf{x} = (x_1, x_2)$.<br>
# 우리는 두 집합의 각 원소에 대해 $\textbf{x} = (x_1, x_2)$ 두가지 값을 측정할 수 있다.
# * Can we decide which entry belongs to which set based on these two measurements?<br>이 두 측정값을 이용하여 어떤 원소가 어떤 집합에 속하는지 알 수 있을까?
#
#

# %%


# %%
import functools
import os
from typing import Dict, List, Tuple, Union


import matplotlib.pyplot as plt
import numpy as np
import numpy.random as nr
import pandas as pd
import scipy.optimize as so



# %%
# to save CI time

if os.getenv('CI', False):
    options = {'maxiter': 10}
else:
    options = None



# %% [markdown]
# $(x_1, x_2)$ 데이터 집합 두개 생성<br>Generating two data sets
#
#

# %%
set_0_bar = (1, 0)
set_1_bar = (0, 1)



# %%
n = 2000
ndim = 2

set_0 = nr.normal(set_0_bar, [1, 1], (n//2, 2))
set_1 = nr.normal(set_1_bar, [1, 1], (n//2, 2))



# %% [markdown]
# 생성한 두 데이터 집합을 표시<br>
# Visualizing the two data sets
#
#

# %%
def plot_two_sets(set_a, set_b, set_a_x_bar=set_0_bar, set_b_x_bar=set_1_bar):

    plt.plot(set_a[:, 0], set_a[:, 1], '.', label="y=0", alpha=0.5)
    plt.plot(set_b[:, 0], set_b[:, 1], '+', label="y=1", alpha=0.5)

    plt.plot(set_a_x_bar[0], set_a_x_bar[1], 'kx')
    plt.plot(set_b_x_bar[0], set_b_x_bar[1], 'kx')

    plt.grid(True)
    plt.axis('equal')
    plt.xlabel("$x_1$")
    plt.ylabel("$x_2$")



# %%
# plot_two_sets(set_0, set_1, set_0_bar, set_1_bar)

# xlim_data = plt.xlim()
# ylim_data = plt.ylim()

# plt.legend(loc=0)
# plt.show()
# plt.close();



# %% [markdown]
# ## 데이터 준비<br>Prepare data
#
#

# %% [markdown]
# ### Individual population<br>개별 데이터 포인트
#
#

# %% [markdown]
# Collect all measurements & labels (set number) into one `numpy.ndarray`<br>
# 모든 측정 값과 소속 집합 이름표 라벨을 하나의 배열 안에 모음
#
#

# %% [markdown]
# | measurement 측정값 | label 라벨 |
# |:----------:|:-----------:|
# | $(x_1, x_2)$ | 0 |
# | $(x_1, x_2)$ | 1 |
#
#

# %%
y0 = np.zeros((len(set_0), 1))
y1 = np.ones((len(set_1), 1))

data_0 = np.concatenate([set_0, y0], axis=1)
data_1 = np.concatenate([set_1, y1], axis=1)

data = np.concatenate([
        data_0,
        data_1
    ], axis=0
)



# %% [markdown]
# 행과 열의 갯수 확인<br>
# Check the number of rows and columns
#
#

# %%
data.shape



# %% [markdown]
# 처음 10개의 data<br>First 10 data points
#
#

# %%
data[:10, :]



# %% [markdown]
# 마지막 10개의 data<br>Last 10 data points
#
#

# %%
data[-10:, :]



# %% [markdown]
# ### Histogram 히스토그램
#
#
#

# %%
HistogramDict = Dict[int, np.ndarray]
EdgeList = List[np.ndarray]
EdgeDict = Dict[int, EdgeList]


def calc_2d_histograms(
    data:np.ndarray,
    n_bins_list:Tuple[int]=(30, 40),
    ranges:Tuple[Tuple[float]]=((-3.0, +3.0), (-4.0, +4.0),),
) -> List[Union[HistogramDict, EdgeList]]:
    '''
    Calculate histograms from the data population
    '''
    n_pop = data.shape[0]
    ndim = data.shape[1] - 1

    if isinstance(n_bins_list, int):
        n_bins_list = (n_bins_list,) * ndim

    # validate input arguments
    assert all(
        map(
            lambda r:len(r) == ndim,
            ranges
        )
    ), f'ranges = {ranges}'

    label_list = np.unique(data[:, -1])

    hist_dict = {}

    edges_dict = {}

    population_dict = {}

    for label in label_list:
        # histogram for i'th class
        data_label = data[data[:,-1] == label,:]
        assert data_label.shape[1] == (ndim+1), (
            f"data_label.shape = {data_label.shape}\nndim = {ndim}"
        )
        population_dict[label] = data_label.shape[0]

        histogram_label, edges_label = np.histogramdd(
            data_label[:, :-1],
            bins=n_bins_list,
            range=ranges,
        )
        hist_dict[label] = histogram_label # in the shape of (n_bins_list[0], n_bins_list[1])
        assert histogram_label.shape == tuple(n_bins_list), (
            f"label = {label}\n"
            f"histogram_label.shape = {histogram_label.shape}\n"
            f"n_bins_list = {n_bins_list}\n"
        )
        edges_dict[label] = edges_label

    assert sum(population_dict.values()) == n_pop, (
        f"n_pop = {n_pop}\n"
        f"spopulation_dict = {population_dict}\n"
    )

    # verify all histograms have the same edges
    for label in label_list[1:]:
        edge_list = edges_dict[label]
        for axis, (edge, edge_first) in enumerate(zip(edge_list, edges_dict[label_list[0]])):
            assert np.allclose(edge, edge_first),(
                f"label = {label}\n"
                f"axis = {axis}\n"
                f"edges_dict[label] = {edges_dict[label]}\n"
                f"edges_dict[label_list[0]] = {edges_dict[label_list[0]]}\n"
            )

    return [hist_dict, edges_dict[label]]


# %%
hist_dict, edges_list = calc_2d_histograms(data)



# %%
def edges_to_nodes(edges_list:EdgeList,) -> np.ndarray:
    '''
    Convert edges to nodes

    Parameters
    ----------
    edges_list : List[axis_0_array, axis_1_array, ...]

    Returns
    -------
    np.ndarray
        shape = (n_nodes, n_axes)
        n_nodes = (n_bins_0 - 1) * (n_bins_1 - 1) * ...
    '''
    ndim = len(edges_list)

    lower_mesh = np.array(
        np.meshgrid(
            *[edge[:-1] for edge in edges_list],
            indexing='ij'
        )
    ).T.reshape(-1, ndim)
    assert lower_mesh.shape[1] == ndim, (
        f"lower_mesh.shape = {lower_mesh.shape}\n"
        f"len(edges_list) = {ndim}\n"
        f"[len(edge)] = {[len(edge) for edge in edges_list]}\n"
    )
    upper_mesh = np.array(
        np.meshgrid(
            *[edge[1:] for edge in edges_list],
            indexing='ij'
        )
    ).T.reshape(-1, ndim)

    node_mesh = (lower_mesh + upper_mesh) * 0.5
    result = np.hstack((node_mesh, lower_mesh, upper_mesh))
    assert result.shape[1] == (ndim * 3), (
        f"result.shape = {result.shape}\n"
        f"ndim = {ndim}\n"
    )

    return result


# %%
def test_edges_to_nodes():
    edges_list = [
        np.array([0, 1, 2, 3]),
        np.array([-3, -2, -1,]),
    ]

    ndim = 2

    nodes = edges_to_nodes(edges_list)

    assert nodes.shape == (6, ndim * 3), (
        f"nodes.shape = {nodes.shape}\n"
        f"nodes = {nodes}\n"
    )

    expected_nodes = np.array([
        [0.5, -2.5, 0.0, -3.0, 1.0, -2.0],
        [1.5, -2.5, 1.0, -3.0, 2.0, -2.0],
        [2.5, -2.5, 2.0, -3.0, 3.0, -2.0],
        [0.5, -1.5, 0.0, -2.0, 1.0, -1.0],
        [1.5, -1.5, 1.0, -2.0, 2.0, -1.0],
        [2.5, -1.5, 2.0, -2.0, 3.0, -1.0],
    ])   # nodes    # lower    #upper

    assert np.allclose(nodes, expected_nodes), (
        f"nodes = \n{nodes}\n"
        f"expected_nodes = \n{expected_nodes}\n"
    )

test_edges_to_nodes()


# %%
def nodes_and_weights_from_histogram(
    hist_dict:HistogramDict,
    edge_list:EdgeList,
) -> np.ndarray:
    '''
    Output data format (2D case) :
      x  y x_lower y_lower weight label
    x y can be centerpoint of the bin.
    If bin size is small enough, one corner point can be used instead.
    '''

    ndim = len(edge_list)

    nodes = edges_to_nodes(edges_list)

    assert nodes.shape[1] == (ndim * 3), (
        f"nodes.shape = {nodes.shape}\n"
        f"ndim * 3 = {ndim * 3}\n"
    )

    result_list = []

    # add histograms as weight columns
    for k, weight in hist_dict.items():
        assert nodes.shape[0] == weight.size, (
            f"nodes.shape = {nodes.shape}\n"
            f"weights.size = {weight.size}\n"
        )

        weight_column = weight.reshape(-1, 1)
        result_list.append(
            np.hstack(
                (
                    nodes, weight_column, np.full((nodes.shape[0], 1), k)
                )
            )
        )

    # TODO : remove the rows with weights == 0

    return np.vstack(result_list)


# %%
nodes_and_weights_from_histogram(hist_dict, edges_list)
pass



# %% [markdown]
# ## 첫번째 (순진한) 시도<br>First (naive) attempt
#
#

# %% [markdown]
# ### 모델<br>Model
#
#

# %% [markdown]
# Using a Linear function, estimate $y$ from $x_1$ and $x_2$<br>
# 선형적으로 $x_1$, $x_2$ 로부터 $y$ 값을 추정
#
#

# %% [markdown]
# $$
# \hat y = H(\textbf x)= w_1 x_1 +  x_2 + w_2
# $$
#
#

# %%
def wx(w:np.ndarray, x_y:np.ndarray) -> np.ndarray:
    w1 = w[0]
    w2 = w[1]

    x1 = x_y[:, 0]
    x2 = x_y[:, 1]

    return w1 * x1 + x2 + w2



# %% [markdown]
# 이 $\hat y$ 값이 0.5 보다 크면 1, 아니면 0 인 것으로 가정.<br>Let's assume it was one if this $\hat y$ is larger than 0.5. Zero otherwise.
#

# %% [markdown]
# ### 비용 함수<br>Cost function
#
#

# %% [markdown]
# $$
# C = \frac{1}{n}\sum_{i=1}^{n} \left( \hat y_i - y_i \right)^2
# $$
#

# %% [markdown]
# 예상되는 문제점?<br>
# Can you expect any possible issues?
#
#

# %%
def cost_function_first_attempt(w:np.ndarray, x_y:np.ndarray) -> float:
    n = len(x_y)
    y_hat = wx(w, x_y)
    y = x_y[:, -1]

    error = y_hat - y
    error_sqr = error ** 2
    result = error_sqr.sum() / n

    return result



# %% [markdown]
# Cost function over parameter space ($w_1 \times w_2$ plane)<br>
# 매개변수공간 ($w_1 \times w_2$ 평면) 상의 비용함수
#
#

# %%
@functools.lru_cache
def calc_cost_surf(cost_function):
    w1 = np.linspace(-10.0, 10.0, 20*20+1)
    w2 = np.linspace(-10.0, 10.0, 20*20+1)

    W1, W2 = np.meshgrid(w1, w2)
    C = np.zeros_like(W1)

    for i_row in range(W1.shape[0]):
        for j_col in range(W1.shape[1]):
            w = np.array([W1[i_row, j_col], W2[i_row, j_col]])
            C[i_row, j_col] = cost_function(w, data)

    return W1, W2, C



# %%
def plot_cost_surf(cost_function):

    W1, W2, C = calc_cost_surf(cost_function)

    fig = plt.figure(figsize=(10, 5))

    ax0 = fig.add_subplot(1, 2, 1)
    ax0.contour(W1, W2, C, cmap='viridis')
    ax0.set_xlabel('$w_1$')
    ax0.set_ylabel('$w_2$')
    ax0.axis('equal')
    ax0.grid(True)

    ax1 = fig.add_subplot(1, 2, 2, projection='3d')
    ax1.plot_surface(W1, W2, C, cmap='viridis')
    ax1.set_xlabel('$w_1$')
    ax1.set_ylabel('$w_2$')

    return ax0, ax1



# %%
axs = plot_cost_surf(cost_function_first_attempt)



# %% [markdown]
# 최적화<br>
# Optimize
#
#

# %%
def get_callback(weight_list=[], cost_list=[]):
  def callback(intermediate_result:so.OptimizeResult):
    assert isinstance(intermediate_result, so.OptimizeResult), (
        f"expected type : {so.OptimizeResult}\n"
        f"passed type : {type(intermediate_result)}\n"
    )
    weight_list.append(intermediate_result.x)
    cost_list.append(intermediate_result.fun)

  return callback



# %%
weight_list_linear = []
cost_list_linear = []

result = so.minimize(
    cost_function_first_attempt,
    x0=np.array([-5.0, 10.0]),
    args=(data,),
    method="Nelder-Mead",
    callback=get_callback(weight_list_linear, cost_list_linear),
)



# %%
result

# %%
weights = result.x
cost_value = result.fun
n_iter = result.nit
n_call = result.nfev
warning = result.message

result



# %%
plt.plot(cost_list_linear, '.-', label='linear')
plt.xlabel('iter')
plt.ylabel('cost')
plt.legend(loc=0)
plt.grid(True)



# %% [markdown]
# Decision bounday satsfying $\hat y = 0.5$<br>
# 0 과 1이 나누어지는 경계 : $\hat y = 0.5$
#
#

# %% [markdown]
# $$
# \begin{align}
#     \hat y &= 0.5 \\
#     w_1 x_1 +  x_2 + w_2 &= 0.5 \\
#      x_2 &= -w_1 x_1 -w_2 + 0.5
# \end{align}
# $$
#
#

# %%
def plot_decision_boundary(x_min, x_max, weights_array):
    x1_array = np.linspace(x_min, x_max)
    x2_array = - weights_array[0] * x1_array - weights_array[1] + 0.5

    plt.plot(x1_array, x2_array, label="$\hat y = 0.5$")



# %%
plot_two_sets(set_0, set_1)
plot_decision_boundary(data[:, 0].min(), data[:, 0].max(), weights)

plt.legend(loc=0)
plt.show()
plt.close();



# %%
axs = plot_cost_surf(cost_function_first_attempt)

weight_array = np.array(weight_list_linear)

axs[0].plot(weight_array[:, 0], weight_array[:, 1], 'C1');
axs[1].plot(weight_array[:, 0], weight_array[:, 1], cost_list_linear, 'C1');



# %% [markdown]
# ## Second attempt : Step function<br>두번째 시도 : 계단함수
#
#

# %% [markdown]
# 0 또는 1로 바꾸어주는 함수<br>
# A function generating 0 or 1<br>
#
#

# %% [markdown]
# $$
# s(z)=
#     \begin{cases}
#         0, z < 0\\
#         1, z >= 0 \\
#     \end{cases}
# $$
#
#

# %%
def step(z):
    return np.heaviside(z, 0)



# %%
z_array = np.linspace(-10, 10)
g_z_array = step(z_array)
plt.plot(z_array, g_z_array)
plt.grid(True)
plt.xlabel('$z$')
plt.ylabel('$g(z)$')
plt.show()



# %% [markdown]
# 계단 함수를 사용하는 비용함수<br>
# Cost function using the sigmoid function
#
#

# %% [markdown]
# $$
# \begin{align}
#     H(\textbf x) &= s(w_1 x_1 +  x_2 + w_2)\\
#     cost(w_1, w_2) &= \frac{1}{n} \sum_{i=1}^n {\left(H(\textbf{x}_i) - y_i\right)^2}
# \end{align}
# $$
#

# %%
def cost_function_step(w:np.ndarray, x_y:np.ndarray) -> float:
    n = len(x_y)
    y_hat = step(wx(w, x_y))
    y = x_y[:, -1]

    error = y_hat - y
    error_sqr = error ** 2
    result = error_sqr.sum() / n

    return result



# %% [markdown]
# Cost function over parameter space ($w_1 \times w_2$ plane)<br>
# 매개변수공간 ($w_1 \times w_2$ 평면) 상의 비용함수
#
#

# %%
plot_cost_surf(cost_function_step)



# %% [markdown]
# 최적화<br>
# Optimize
#
#

# %%
weights_list_step = []
cost_list_step = []

result = so.minimize(
    cost_function_step,
    x0=np.array([-5.0, 10.0]),
    args=(data,),
    method="Nelder-Mead",
    callback=get_callback(weights_list_step, cost_list_step),
    options=options,
)

weights = result.x
cost_value = result.fun
n_iter = result.nit
n_call = result.nfev
warning = result.message

result



# %%
plt.plot(cost_list_linear, '.-', label='linear')
plt.plot(cost_list_step, '.-', label='step')
plt.xlabel('iter')
plt.ylabel('cost')
plt.legend(loc=0)
plt.grid(True)



# %%
plot_two_sets(set_0, set_1)
plot_decision_boundary(data[:, 0].min(), data[:, 0].max(), weights)

plt.xlim(xlim_data)
plt.ylim(ylim_data)

plt.legend(loc=0)
plt.show()
plt.close();



# %%
weights_array_step = np.array(weights_list_step)
axs = plot_cost_surf(cost_function_step)
axs[0].plot(
    weights_array_step[:, 0], weights_array_step[:, 1], 'C1'
);
axs[1].plot(
    weights_array_step[:, 0], weights_array_step[:, 1],
    cost_list_step,
    'C1'
);



# %% [markdown]
# ## Third attempt : Sigmoid function<br>세번째 시도 : 시그모이드 함수
#
#

# %% [markdown]
# 0 과 1 사이를 부드럽게 연결하는 함수<br>
# A function connecting 0 and 1 smoothly<br>
# ref : [![youtube](https://i.ytimg.com/vi/PIjno6paszY/hqdefault.jpg)](https://youtu.be/PIjno6paszY?t=650)
#
#

# %% [markdown]
# $$
# z = w_1 x_1 +  x_2 + w_2
# $$
#
#

# %% [markdown]
# $$
# \hat y =  g(z)=\frac{1}{1+exp\left(-z\right)}
# $$
#
#

# %% [markdown]
# $$
# C = \frac{1}{n}\sum_{i=1}^{n} \left( \hat y_i - y_i \right)^2
# $$
#

# %%
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))



# %%
z_array = np.linspace(-10, 10)
g_z_array = sigmoid(z_array)
plt.plot(z_array, g_z_array)
plt.grid(True)
plt.xlabel('$z$')
plt.ylabel("$g(z)$")
plt.show()



# %% [markdown]
# 시그모이드 함수를 사용하는 비용함수<br>
# Cost function using the sigmoid function
#
#

# %%
def cost_function_sigmoid(w:np.ndarray, x_y:np.ndarray) -> float:
    n = len(x_y)
    y_hat = sigmoid(wx(w, x_y))
    y = x_y[:, -1]

    error = y_hat - y
    error_sqr = error ** 2
    result = error_sqr.sum() / n

    return result



# %% [markdown]
# Cost function over parameter space ($w_1 \times w_2$ plane)<br>
# 매개변수공간 ($w_1 \times w_2$ 평면) 상의 비용함수
#
#

# %%
axs = plot_cost_surf(cost_function_sigmoid)



# %% [markdown]
# 최적화<br>
# Optimize
#
#

# %%
weight_list_sigmoid = []
cost_list_sigmoid = []

result = so.minimize(
    cost_function_sigmoid,
    x0=np.array([10.0, 5.0]),
    args=(data,),
    method="Nelder-Mead",
    callback=get_callback(weight_list_sigmoid, cost_list_sigmoid),
    options=options,
)

weights = result.x
cost_value = result.fun
n_iter = result.nit
n_call = result.nfev
warning = result.message

result



# %%
plt.plot(cost_list_linear, '.-', label='linear')
plt.plot(cost_list_step, '.-', label='step')
plt.plot(cost_list_sigmoid, '.-', label='sigmoid')
plt.xlabel('iter')
plt.ylabel('cost')
plt.legend(loc=0)
plt.grid(True)



# %%
plot_two_sets(set_0, set_1)
plot_decision_boundary(data[:, 0].min(), data[:, 0].max(), weights)

plt.legend(loc=0)
plt.show()
plt.close();



# %%
weights_array_sigmoind = np.array(weight_list_sigmoid)

axs = plot_cost_surf(cost_function_sigmoid)
axs[0].plot(
    weights_array_sigmoind[:, 0],
    weights_array_sigmoind[:, 1],
    'C1'
);
axs[1].plot(
    weights_array_sigmoind[:, 0],
    weights_array_sigmoind[:, 1],
    cost_list_sigmoid,
    'C1'
);



# %% [markdown]
# ## 교차 엔트로피 비용함수<br>Cross entropy cost function
#
#

# %% [markdown]
# 국소 최소점을 피해 전역 최소점을 찾기 위해 사용<br>To find global and avoid local minimum.
#
#

# %% [markdown]
# ref : (14:23)
# [![youtube](https://i.ytimg.com/vi/6vzchGYEJBc/hqdefault.jpg)](https://youtu.be/6vzchGYEJBc)
#
#

# %% [markdown]
# $$
# C = \frac{1}{n}\sum_{i=1}^{n} \left[ -y_i log \left( \hat y_i \right) - \left(1 - y_i \right) log \left( 1 - \hat y_i \right)\right]
# $$
#

# %%
def cost_function_cross_entropy(w:np.ndarray, x_y:np.ndarray) -> float:
    n = len(x_y)
    y_hat = sigmoid(wx(w, x_y))
    y = x_y[:, -1]

    cost = -y * np.log2(y_hat) - (1 - y) * np.log2(1 - y_hat)

    return np.mean(cost)



# %% [markdown]
# Cost function over parameter space ($w_1 \times w_2$ plane)<br>
# 매개변수공간 ($w_1 \times w_2$ 평면) 상의 비용함수
#
#

# %%
axs = plot_cost_surf(cost_function_cross_entropy)



# %% [markdown]
# 최적화<br>
# Optimize
#
#

# %%
weights_list_cross_entropy = []
cost_list_cross_entropy = []

result = so.minimize(
    cost_function_cross_entropy,
    x0=np.array([-5.0, 10.0]),
    args=(data,),
    method="Nelder-Mead",
    callback=get_callback(weights_list_cross_entropy, cost_list_cross_entropy),
    options=options,
)

weights = result.x
cost_value = result.fun
n_iter = result.nit
n_call = result.nfev
warning = result.message

result



# %%
plt.plot(cost_list_linear, '.-', label='linear')
plt.plot(cost_list_step, '.-', label='step')
plt.plot(cost_list_sigmoid, '.-', label='sigmoid')
plt.plot(cost_list_cross_entropy, '.-', label='cross entropy')
plt.xlabel('iter')
plt.ylabel('cost')
plt.legend(loc=0)
plt.grid(True)



# %%
plot_two_sets(set_0, set_1)
plot_decision_boundary(data[:, 0].min(), data[:, 0].max(), weights)

plt.legend(loc=0)

plt.show()
plt.close();



# %%
weights_array_cross_entropy = np.array(weights_list_cross_entropy)

axs = plot_cost_surf(cost_function_cross_entropy)

axs[0].plot(
    weights_array_cross_entropy[:, 0],
    weights_array_cross_entropy[:, 1],
    'C1'
);
axs[1].plot(
    weights_array_cross_entropy[:, 0],
    weights_array_cross_entropy[:, 1],
    cost_list_cross_entropy,
    'C1'
);



# %% [markdown]
# ## scikit-learn
# A library more specialized to (computational) machine learning<br>
# 보다 (전산) 기계 학습에 더 특화된 라이브러리
#
#

# %% [markdown]
# ref :
# * [[0](https://scikit-learn.org/stable/modules/lda_qda.html)] description
# * [[1](https://scikit-learn.org/stable/auto_examples/classification/plot_lda_qda.html)] example
#

# %%
import sklearn.discriminant_analysis as sd
lda = sd.LinearDiscriminantAnalysis(solver="svd", store_covariance=True)

X = data[:, :2]
y = data[:, 2]

lda.fit(X, y)



# %%
def plot_mesh_pred(lda, x_min, x_max, y_min, y_max, nx=100, ny=100):

    x_mesh, y_mesh = np.meshgrid(
        np.linspace(x_min, x_max, nx),
        np.linspace(y_min, y_max, ny),
    )

    xy_mesh_columns = np.c_[x_mesh.ravel(), y_mesh.ravel()]

    z_column = lda.predict_proba(xy_mesh_columns)

    z_mesh = z_column[:, 1].reshape(x_mesh.shape)

    plt.pcolor(x_mesh, y_mesh, z_mesh, shading="auto")
    plt.contour(x_mesh, y_mesh, z_mesh, [0.5], colors="white")

    plt.grid(True)



# %%
plot_two_sets(set_0, set_1)
plot_mesh_pred(lda, -10, 10, -6, 10)

plt.legend(loc=0)
plt.show()
plt.close();



# %% [markdown]
# ## Tensorflow
# A library specialized in neural networks<br>인공신경망에 특화된 라이브러리
#
#

# %% [markdown]
# Got some help from https://chat.openai.com to generate following code.<br>
# 아래의 코드를 생성하기 위해 일부 https://chat.openai.com 의 도움을 받았음.
#
#

# %%
import numpy as np
import tensorflow as tf


X = data[:, :2]
y = data[:, 2]


# Define the model architecture
tf_model = tf.keras.Sequential([
  tf.keras.layers.Dense(1, input_shape=(2,), activation='sigmoid',)
])


# Compile the model
tf_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


# Train the model
n_epoch = 50

# To save time when automatically testing the SW
if os.getenv('CI', False):
    n_epoch = 1

tf_model.fit(X, y, epochs=50, batch_size=10)


# Evaluate the model
loss, accuracy = tf_model.evaluate(X, y)
print("Accuracy:", accuracy)


# %%
def plot_decision_boundary_tf(tf_model, x_min, x_max, nx=100):

    x_array = np.linspace(x_min, x_max, nx)

    weights, bias = tf_model.get_weights()

    # w0 x0 + w1 x1 + bias
    # -> x1 = -(w0/w1) x0 - bias/w1
    slope = -weights[0] / weights[1]
    intercept = -bias / weights[1]

    decision_bounday = slope * x_array + intercept
    plt.plot(x_array, decision_bounday, 'k-')

    plt.grid(True)



# %%
plot_two_sets(set_0, set_1)
plot_decision_boundary_tf(
    tf_model,
    *(plt.gca().get_xlim())
)



# %% [markdown]
# ## PyTorch
#
# I got help from https://gemini.google.com to write the code below.<br>
# 아래 코드 작성을 위해 https://gemini.google.com 로 부터 도움을 받았음.
#
#

# %%
import torch
import torch.nn
import torch.optim


# Datasets
X = torch.tensor(data[:, :2], dtype=torch.float32)
y = torch.tensor(data[:, 2], dtype=torch.float32)


# Model
class MyModel(torch.nn.Module):  # PyTorch models are usually defined as classes
    def __init__(self, in_dim=2, out_dim=1):
        super(MyModel, self).__init__()
        self.linear = torch.nn.Linear(in_dim, out_dim)  # Equivalent to Dense layer

    def forward(self, x):
        x = self.linear(x)
        return torch.sigmoid(x)


def train(model, X, y, optimizer, criterion, n_epoch=50):

    epoch_list = []
    loss_list = []

    if os.getenv('CI', False):  # CI environment check
        n_epoch = 1

    for epoch in range(n_epoch):
        total = 0
        for i in range(0, len(X), 10):  # Batching
            batch_X = X[i:i+10]
            batch_y = y[i:i+10]

            output = model(batch_X)
            loss = criterion(output.squeeze(1), batch_y)  # squeeze for BCEWithLogitsLoss

            total += loss.item()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        loss_list.append(total)

    return loss_list


torch_model = MyModel()

cost_list_torch = train(
    torch_model, X, y,
    optimizer=torch.optim.Adam(torch_model.parameters()),
    criterion=torch.nn.BCELoss()
)



# %%
def plot_decision_boundary_pytorch(pytorch_model, x_min, x_max, nx=100):
    x_array = np.linspace(x_min, x_max, nx)

    # Extract weights and bias (assuming a two-input linear model)
    weights = pytorch_model.linear.weight.detach().numpy()[0]  # Access parameters
    bias = pytorch_model.linear.bias.detach().numpy()

    slope = -weights[0] / weights[1]
    intercept = -bias / weights[1]

    decision_boundary = slope * x_array + intercept
    plt.plot(x_array, decision_boundary, 'k-')

    plt.grid(True)



# %%
plt.plot(cost_list_linear, '.-', label='linear')
plt.plot(cost_list_step, '.-', label='step')
plt.plot(cost_list_sigmoid, '.-', label='sigmoid')
plt.plot(cost_list_cross_entropy, '.-', label='cross entropy')
plt.plot(cost_list_torch, '.-', label='pytorch mini-batch')
plt.xlabel('iter')
plt.ylabel('cost')
plt.legend(loc=0)
plt.grid(True)



# %%
# Example usage with the 'model' defined earlier
plot_two_sets(set_0, set_1)  # You'll need to define how to plot these sets
plot_decision_boundary_pytorch(
    torch_model,
    *(plt.gca().get_xlim())
)



# %% [markdown]
# ## Final Bell<br>마지막 종
#
#

# %%
# stackoverfow.com/a/24634221
import os
os.system("printf '\a'");



# %% [markdown]
# ## References<br>참고문헌
# * J. Santarcangelo, Deep Neural Networks with PyTorch, Coursera
# * S. Kim, Deep Learning for Everyone, http://hunkim.github.io/ml/
# * SciPy Developer Community, Optimization and root finding, SciPy Documentation, https://docs.scipy.org/doc/scipy/reference/optimize.html
#
#

# %%



