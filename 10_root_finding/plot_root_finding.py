# 무작위 수 모듈
# Random number module
import numpy.random as nr
import pylab as py


# Initialize random number generator
# 난수 발생기 초기화
nr.seed()


def plot(f, x_start, x_end, x_interval=None, epsilon=0.15):
    if x_interval is None:
        x_interval = x_end - x_start

    x = py.arange(x_start, x_end+0.1*x_interval, x_interval)
    # y = x^2
    py.plot(x, f(x), 'ko', label='$y=x^2-10$')
    # y = 0
    py.plot(x, py.zeros_like(x), 'ro', label='$y=0$')

    # +/- epsilon
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
    py.plot(x_array, df_dx(x_array), 'b.', label=r'$\frac{df}{dx}$')

    # 범례 표시
    # Show legend
    py.legend()


def plot_one_tangent(f, df_dx, x_i, x_interval):
    y_i = f(x_i)
    slope = df_dx(x_i)
    
    x_tangent_array = py.linspace(x_i - x_interval * 2, x_i + x_interval * 2, 4+1)
    y_tangent_array = slope * (x_tangent_array - x_i) + y_i
    
    py.plot(x_tangent_array, y_tangent_array, color=nr.random(3), alpha=0.5)


def plot_many_tangents(f, df_dx, x_array):

    x_interval = x_array[1] - x_array[0]

    for x_i in x_array:
        
        plot_one_tangent(f, df_dx, x_i, x_interval)
