import pylab as py


def num_int_0(f, xi, xe, n):
    x_array = py.linspace(xi, xe, n+1)
    delta_x = x_array[1] - x_array[0]

    integration_result = 0.0
    for k in range(n):
        integration_result += f(x_array[k]) * delta_x

    return integration_result


def num_int_1(f, xi, xe, n):
    x_array = py.linspace(xi, xe, n+1)
    delta_x = x_array[1] - x_array[0]

    integration_result = 0.0
    y_k = f(x_array[0])

    for k in range(n):
        y_k_plus_1 = f(x_array[k+1])
        integration_result += 0.5 * (y_k + y_k_plus_1) * delta_x
        y_k = y_k_plus_1

    return integration_result


def num_int_2(f, xi, xe, n):
    if n % 2:
        n += 1

    x_array = py.linspace(xi, xe, n+1)
    delta_x = x_array[1] - x_array[0]
    delta_x_third = delta_x / 3.0

    integration_result = 0.0
    y0 = f(x_array[0])

    for i in range(1, n, 2):
        y1 = f(x_array[i])
        y2 = f(x_array[i+1])
        integration_result += delta_x_third * (y0 + 4*y1 + y2)
        y0 = y2

    return integration_result
