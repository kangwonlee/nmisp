def euler_step(f, x0, t0, t1):
    """
    One time step of Euler method

    f  : function dx_dt(t0, x0)
    x0 : initial condition
    t0 : this step time
    t1 : next step time
    """

    # time step
    delta_t = t1 - t0

    # slope
    s1 = f(t0, x0)

    # next step
    x1 = x0 + s1 * delta_t

    return x1


def euler(dx_dt, t_array, x_0):

    time_list, result_list = ode_solver(euler_step, dx_dt, t_array, x_0)

    return time_list, result_list


def heun_step(f, x0, t0, t1):
    """
    One time step of Heun's method

    f  : function dx_dt(t0, x0)
    x0 : initial condition
    t0 : this step time
    t1 : next step time
    """

    # time step
    delta_t = t1 - t0

    # slope
    s1 = f(t0, x0)

    # next step by Euler
    x1_euler = x0 + s1 * delta_t

    # slope at next step
    s2 = f(t1, x1_euler)

    # average of two slopes
    s_average = (s1 + s2) * 0.5

    # next step by Heun's method
    x1 = x0 + s_average * delta_t

    return x1


def heun(dx_dt, t_array, x_0):

    time_list, result_list = ode_solver(heun_step, dx_dt, t_array, x_0)

    return time_list, result_list


def rk4_step(f, x0, t0, t1):
    """
    One time step of Runge-Kutta method

    f  : function dx_dt(t0, x0)
    x0 : initial condition
    t0 : this step time
    t1 : next step time
    """
    delta_t = (t1 - t0)
    delta_t_half = delta_t * 0.5
    t_half = t0 + delta_t_half
    
    # Step 1
    s1 = f(t0, x0)

    # Step 2
    s2 = f(t_half, x0 + s1 * delta_t_half)

    # Step 3
    s3 = f(t_half, x0 + s2 * delta_t_half)

    # Step 4
    s4 = f(t1, x0 + s3 * delta_t)

    # Step 5
    s = (1.0 / 6.0) * (s1 + (s2 + s3) * 2 + s4)

    # Step 6
    x1 = x0 + s * delta_t

    return x1


def rk4(dx_dt, t_array, x_0):

    time_list, result_list = ode_solver(rk4_step, dx_dt, t_array, x_0)

    return time_list, result_list


def ode_solver(step, dx_dt, t_array, x_0):
    time_list = [t_array[0]]
    result_list = [x_0]

    x_i = x_0

    for k, t_i in enumerate(t_array[:-1]):
        # time step
        x_i_plus_1 = step(dx_dt, x_i, t_i, t_array[k+1])

        time_list.append(t_array[k+1])
        result_list.append(x_i_plus_1)
        
        x_i = x_i_plus_1

    return time_list, result_list
