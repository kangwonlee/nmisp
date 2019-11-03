import numpy as np
import matplotlib.pyplot as plt
import functools


def assert_almost_equal(expected, result, relative_error=1e-3):
    assert relative_error > abs(expected - result)/expected, (f"expected = {expected} result = {result}")


@functools.lru_cache(10)
def radius_square_of_half_circle_area(area=1):
    result = 2 * area / np.pi

    assert_almost_equal(area, result*np.pi*0.5)

    return result


@functools.lru_cache(10)
def radius_of_half_circle_area(area=1):
    result = radius_square_of_half_circle_area(area) ** 0.5

    assert_almost_equal(area, (result**2)*np.pi*0.5)

    return result


def half_circle(x, half_circle_area=1.0):
    return np.sqrt(np.abs(radius_square_of_half_circle_area(half_circle_area) - x**2))


def axis_equal_grid_True():
    plt.axis('equal')
    plt.grid(True)


def plot_half_circle_with_stems(n=10, half_circle_area=1):
    plot_half_circle_theta_space(half_circle_area)

    plot_half_circle_stems(n, half_circle_area)

    axis_equal_grid_True()


def plot_half_circle_stems(n, half_circle_area):
    x_array_bar, y_array_bar = get_half_circle_xy_linspace(n, half_circle_area)

    # https://stackoverflow.com/40896356
    plt.stem(x_array_bar, y_array_bar, markerfmt='.')
    # For anaconda 2019.07 or later
    # plt.stem(x_array_bar, y_array_bar, markerfmt='.', use_line_collection=True)


def plot_half_circle_theta_space(half_circle_area):
    x_array, y_plus = get_half_circle_xy_theta_space(half_circle_area)
    plt.plot(x_array, y_plus)


def get_half_circle_xy_linspace(n, half_circle_area):
    x_array_bar = linspace_r(radius_of_half_circle_area(half_circle_area), n+1)
    y_array_bar = half_circle(x_array_bar)
    return x_array_bar, y_array_bar


def linspace_r(r, n):
    return np.linspace(-r, r, n)


@functools.lru_cache()
def theta_space(begin:int=180, end:int=0, n:int=None):

    assert isinstance(begin, int)
    assert isinstance(end, int)

    if n is None:
        n = int(abs(end - begin))

    assert isinstance(n, int)

    theta_deg_array = np.linspace(begin, end, n+1)
    theta_rad_array = np.deg2rad(theta_deg_array)

    return np.cos(theta_rad_array)


def plot_a_half_circle_of_area(area=1):
    x_array, y_plus = get_half_circle_xy_theta_space(area)

    plt.fill_between(x_array, y_plus)


def get_half_circle_xy_theta_space(area):
    x_array = radius_of_half_circle_area(area) * theta_space(180, 0)
    y_plus = half_circle(x_array, area)
    return x_array, y_plus
