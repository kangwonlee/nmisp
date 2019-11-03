import numpy as np
import matplotlib.pyplot as plt


def half_circle(x, half_circle_area=1.0):
    return np.sqrt(np.abs(2 * half_circle_area / np.pi - x**2))


def plot_half_circle(n=10, r=1):
    theta_deg_array = np.linspace(180, 0, 180+1)
    theta_rad_array = np.deg2rad(theta_deg_array)

    x_array = r * np.cos(theta_rad_array)
    y_plus = half_circle(x_array)
    y_minus = -y_plus

    plt.plot(x_array, y_plus)
    plt.plot(x_array, y_minus)

    x_array_bar = np.linspace(-r, r, n+1)
    y_array_bar = half_circle(x_array_bar)

    # https://stackoverflow.com/40896356
    plt.stem(x_array_bar, y_array_bar, markerfmt='.', use_line_collection=True)

    plt.axis('equal')
    plt.grid(True)
