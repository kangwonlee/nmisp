def forward_euler_step(f, x0, t0, t1):
    """
    One time step of Forward Euler method

    f:   function dx_dt(x0, t0)
    x0 : initial condition
    t0 : this step time
    t1 : next step time
    """

    # time step
    delta_t = t1 - t0

    # slope
    s1 = f(x0, t0)

    # next step
    x1 = x0 + s1 * delta_t

    return x1


def forward_euler(dx_dt, t_array, x_0):
    time_list = [t_array[0]]
    result_list = [x_0]

    x_i = x_0

    for k, t_i in enumerate(t_array[:-1]):
        # time step
        x_i_plus_1 = forward_euler_step(dx_dt, x_i, t_i, t_array[k+1])

        time_list.append(t_array[k+1])
        result_list.append(x_i_plus_1)
        
        x_i = x_i_plus_1

    return time_list, result_list
