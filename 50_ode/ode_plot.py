import dataclasses

import numpy as np
import pylab as py


@dataclasses.dataclass
class ExactPlotterFirstOrderODE(object):
    """
    a_x x_dot + a_1 x = 0

    see : https://realpython.com/python-data-classes/

    """

    t_array : py.ndarray
    a_0 : float = 2.0
    a_1 : float = 1.0
    x_0 : float = 4.5
    label : str = 'exact'

    def __post_init__(self):
        self.a_ratio = - (self.a_1 / self.a_0)
        self.x_array = self.exact(self.t_array)

    def exact(self, t):
        return self.x_0 * py.exp(self.a_ratio * t)

    def plot(self):
        py.plot(self.t_array, self.x_array, label=self.label)


def ode_slope_1state_interval(func, delta_t, delta_x, te, ti, x_max, x_min):
    time_list = np.arange(ti, te, delta_t)
    x_list = np.arange(x_min, x_max + 0.5 * delta_x, delta_x)
    ode_slope_1state(func, x_list, time_list)
    return time_list


def ode_slope_1state(func, x_list, time_list):
    """
    Plot field of arrows indicating derivatives of the state
    :param func:
    :param x_list:
    :param time_list:
    :return:
    """
    time_mesh, x_mesh = np.meshgrid(time_list, x_list)
    u_mesh = np.ones_like(x_mesh)
    v_mesh = func(time_mesh, x_mesh)
    # magnitude as color
    color_mesh = np.sqrt(u_mesh * u_mesh + v_mesh * v_mesh)

    # https://stackoverflow.com/questions/29589119/plot-width-settings-in-ipython-notebook
    py.figure(figsize=(12, 12))
    py.quiver(time_mesh, x_mesh, u_mesh, v_mesh, color_mesh, angles='xy')

    xy_labels()

    py.xlim((time_list[0] - (time_list[1] - time_list[0]) * 0.125, time_list[-1]))
    py.ylim((min(x_list) - (x_list[1] - x_list[0]) * 0.125,
                max(x_list) + (x_list[-1] - x_list[-2]) * 0.125))
    py.grid(True)


def ode_slopes_2states_cartesian(func, theta_rad_list, theta_dot_rad_list, time_list):
    """
    Plot field of arrows indicating derivatives of the state
    :param func:
    :param theta_rad_list:
    :param theta_dot_rad_list:
    :param time_list:
    :return:
    """

    # cartesian coordinate
    y_rad = np.meshgrid(theta_rad_list, theta_dot_rad_list)

    # derivatives of state at each point
    y_rad_dot = func(time_list, y_rad)

    # color
    color_mesh = np.sqrt(y_rad_dot[0] * y_rad_dot[0] + y_rad_dot[1] * y_rad_dot[1])

    py.figure(figsize=(18, 18))
    py.axis('equal')
    py.quiver(py.rad2deg(y_rad[0]), py.rad2deg(y_rad[1]), py.rad2deg(y_rad_dot[0]), py.rad2deg(y_rad_dot[1]), color_mesh, angles='xy')
    l, r, b, t = py.axis()
    x_span, y2_mesh = r - l, t - b
    py.axis([l - 0.05 * x_span, r + 0.05 * x_span, b - 0.05 * y2_mesh, t + 0.05 * y2_mesh])
    py.grid()


def set_axis(ax, left, right, bottom, top):

    xlims = py.xlim(left=left, right=right)
    ylims = py.ylim(bottom=bottom, top=top,)

    # http://matplotlib.1069221.n5.nabble.com/How-do-I-set-grid-spacing-td9968.html
    ax.set_xticks(np.hstack([np.arange(0, xlims[1]+1, 90), np.arange(-90, xlims[0]-1, -90)]))
    ax.set_yticks(np.hstack([np.arange(0, ylims[1]+1, 90), np.arange(-90, ylims[0]-1, -90)]))


def title_axis_labels(title='Simple pendulum', x_label='$\\theta(deg)$', y_label='$\\frac{d}{dt}\\theta(deg/sec)$'):
    xy_labels(x_label, y_label)
    py.title(title)


def plot_slope_fileds_and_exact_solution(dx_dt, t_array, x_array):
    ode_slope_1state(dx_dt, x_array, t_array)

    exact = ExactPlotterFirstOrderODE(t_array)
    exact.plot()

    py.legend(loc=0, fontsize='xx-large')


def indicate_initial_point(t_0, x_0):
    py.plot(t_0, x_0, 'o')
    py.text(t_0, x_0, '$(t_0, x_0)$')


def get_straight_line_to_next_time_step(t_initial, delta_t, x_initial, slope):
    t_array = py.linspace(t_initial, t_initial + delta_t)
    x_array = slope * (t_array - t_initial) + x_initial

    # (t_2, x_2) point
    t_2, x_2 = t_array[-1], x_array[-1]

    return{'t': t_array, 'x': x_array, 't_e': t_2, 'x_e': x_2}


def format_incremental_plot(x_min=-4, x_max=4, y_min=0, y_max=6):
    py.axis('equal')

    py.xlim(left=x_min, right=x_max)
    py.ylim(bottom=y_min, top=y_max)

    xy_labels()

    py.legend(loc=0)
    py.grid(True)


def xy_labels(x_label='t(sec)', y_label='x(m)'):
    py.xlabel(x_label)
    py.ylabel(y_label)


def get_line_eq(i):
    return f'$x=s_{i}(t-t_{i})+x_{i}$'


def get_point_xy_txt(i):
    return f'$(t_{i}, x_{i})$'


def plot_one_step(t_array, x_array, i):
    py.plot(t_array, x_array, label=get_line_eq(i))

    t_e, x_e = t_array[-1], x_array[-1]

    py.plot(t_e, x_e, 'o')
    text_xy_k(t_e, x_e, i + 1)


def text_xy_k(x, y, k):
    py.text(x, y, get_point_xy_txt(k))
