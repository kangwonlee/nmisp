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


def plot_half_circle(n=10, half_circle_area=1):
    theta_deg_array = np.linspace(180, 0, 180+1)
    theta_rad_array = np.deg2rad(theta_deg_array)

    x_array = radius_of_half_circle_area(half_circle_area) * np.cos(theta_rad_array)
    y_plus = half_circle(x_array)
    y_minus = -y_plus

    plt.plot(x_array, y_plus)
    plt.plot(x_array, y_minus)

    x_array_bar = np.linspace(
        -radius_of_half_circle_area(half_circle_area),
        radius_of_half_circle_area(half_circle_area),
        n+1
    )
    y_array_bar = half_circle(x_array_bar)

    # https://stackoverflow.com/40896356
    plt.stem(x_array_bar, y_array_bar, markerfmt='.', use_line_collection=True)

    plt.axis('equal')
    plt.grid(True)
