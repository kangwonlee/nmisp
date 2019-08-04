import pylab as py


def plot(f, x_start, x_end, x_interval=None):
    if x_interval is None:
        x_interval = x_end - x_start

    x = py.arange(x_start, x_end+0.1*x_interval, x_interval)
    # y = x^2
    py.plot(x, f(x), 'ko', label='$y=x^2-10$')
    # y = 0
    py.plot(x, py.zeros_like(x), 'ro', label='y=0')

    # +/- epsilon
    epsilon=0.15
    py.plot(x, epsilon * py.ones_like(x), 'r-.', label=r'$+\epsilon$')
    py.plot(x, -epsilon * py.ones_like(x), 'r--', label=r'$-\epsilon$')

    # x 축 이름표
    # x axis label
    py.xlabel('x')

    # y 축 이름표
    # y axis label
    py.ylabel('y')

    # 범례 표시
    # Show legend
    py.legend()

    # 모눈 표시
    # Indicate grid
    py.grid()
    
    return x


def plot_derivative(df_dx, x_array):
    # y = 2x
    py.plot(x_array, df_dx(x_array), 'b.', label='$y=2x$')

    # 범례 표시
    # Show legend
    py.legend()
