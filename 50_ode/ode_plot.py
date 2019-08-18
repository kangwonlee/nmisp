import numpy as np
import pylab as py


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
    v_mesh = func(x_mesh, time_mesh)
    # magnitude as color
    color_mesh = np.sqrt(u_mesh * u_mesh + v_mesh * v_mesh)

    # https://stackoverflow.com/questions/29589119/plot-width-settings-in-ipython-notebook
    py.figure(figsize=(12, 12))
    py.quiver(time_mesh, x_mesh, u_mesh, v_mesh, color_mesh, angles='xy')
    py.xlabel('t')
    py.ylabel('x')
    py.xlim((time_list[0] - (time_list[1] - time_list[0]) * 0.125, time_list[-1]))
    py.ylim((min(x_list) - (x_list[1] - x_list[0]) * 0.125,
                max(x_list) + (x_list[-1] - x_list[-2]) * 0.125))
    py.grid(True)


def plot_slope_fileds_and_exact_solution(dx_dt, t_array, x_array, x_exact_array, filename):
    ode_slope_1state(dx_dt, x_array, t_array)
    py.plot(t_array, x_exact_array, label='exact')

    py.legend(loc=0, fontsize='xx-large')

    py.savefig(filename)


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

    py.xlabel('t(sec)')
    py.ylabel('x(m)')

    py.legend(loc=0)
    py.grid(True)


def get_line_eq(i):
    return f'$x=s_{i}(t-t_{i})+x_{i}$'


def get_point_xy_txt(i):
    return f'$(t_{i}, x_{i})$'


def plot_one_step(t_array, x_array, i):
    py.plot(t_array, x_array, label=get_line_eq(i))

    t_e, x_e = t_array[-1], x_array[-1]

    py.plot(t_e, x_e, 'o')
    py.text(t_e, x_e, get_point_xy_txt(i + 1))
