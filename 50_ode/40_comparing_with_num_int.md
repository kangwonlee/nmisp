# Comparison with Numerical Integration<br>수치적분과의 비교


* Let's consider a differential equation of the following form, which represents Newton's second law of motion:<br>다음 미분 방정식을 생각해 보자. 이것은 뉴튼의 두번째 법칙을 나타낸 것이다.

$$
    \frac{d^2x}{dt^2}+0 \cdot \frac{dx}{dt} + 0 \cdot x = \frac{1}{m}f(t)
$$

* This equation tells us that the acceleration of an object is proportional to the net force acting on it.<br>이 식에 따르면, 어떤 물체의 가속도는 그 물체에 가해지는 합력에 비례한다는 것이다.
* To find the object's position $x(t)$, we need to integrate the acceleration twice.<br>해당 물체의 위치 $x(t)$를 찾기 위해서는 가속도를 두 번 적분해야 한다.
* This reveals a deep connection between solving differential equations and numerical integration.<br>이는 미분방정식을 푸는 과정과 수치적분 사이에 깊은 연관성이 있다는 것을 보여준다.

* The table below illustrates this connection by comparing numerical integration methods with their corresponding ODE solvers:<br>아래 표는 수치적분 방법과 그에 대응하는 미분방정식 해법을 비교한 것이다.

|  order  | Numerical Integration       | method | ODE Solver                    |
|:---------:|:--------------------------------:|:--------:|:------------------------------------------------:|
| 0th order | $$ F_k = f(x_k)\cdot \Delta x $$ |  Euler   | $$ x_{k+1} = x_{k} + \Delta t \cdot f(x_k, t_k) $$ |
| 1st order | $$ F_k = \frac{\Delta x}{2}\left[f(x_k) + f(x_{k+1})\right] $$ |  Heun   | $$ x_{k+1} = x_{k} + \frac{\Delta t}{2} \left[f(x_k, t_k) + f(\hat{x}_{k+1}, t_{k+1})\right] $$ |
| 2nd order | $$ F_k = \frac{\Delta x}{6}\left[f(x_k) + 4 \cdot f(x_{k+1}) + f(x_{k+2})\right] $$ |  Runge-Kutta   | $$ x_{k+1} = x_{k} + \frac{\Delta t}{6} \left[f(x_k, t_k) + 2 f(\hat{x}_{k+\frac{1}{2}}, t_{k+\frac{1}{2}})_1+ 2 f(\hat{x}_{k+\frac{1}{2}}, t_{k+\frac{1}{2}})_2 + f(\hat{x}_{k+1}, t_{k+1})\right] $$ |

* Numerical integration and ODE solvers share a fundamental principle: approximating solutions using weighted averages. In numerical integration, these averages are of function values, while in ODE solvers, they are of slopes.<br>수치 적분과 상미분방정식 해법은 모두 기본적으로 가중 평균을 사용하여 해를 근사한다. 수치 적분에서는 함수 값의 평균을 사용하고, 상미분 방정식 해법에서는 기울기의 평균을 사용한다.
* The accuracy of both numerical integration and ODE solvers is characterized by their order. Higher-order methods generally provide more accurate results but may be more computationally expensive.<br>수치적분과 상미분방정식 해법 모두 그 차수가 정확도를 결정한다. 차수가 높은 방법이 일반적으로 더 정확한 결과를 제공하지만, 계산 비용은 더 많이 들 수 있다.
* Consider the simplest methods: 0th order integration uses rectangles to approximate the area under a curve, much like Euler's method for ODEs assumes a constant slope within each interval. Both have first-order accuracy, meaning their global truncation error scales linearly with the step size.<br>가장 간단한 방법 부터 생각해 보자. 0차 적분은 곡선 아래의 면적을 근사하는 데 직사각형을 사용하며, 상미분방정식을 위한 Euler법은 각 구간 내에서 기울기가 일정할 것으로 가정한다. 둘 다 정확도가 1차로, 전역 절단 오차는 간격 길이와 선형적으로 비례한다.
* Moving to higher order: The trapezoidal rule uses trapezoids for integration, analogous to Heun's method, which averages slopes at the interval's endpoints. Both are second-order methods, with global truncation errors that scale quadratically with the step size.<br>좀 더 차수를 높여서, 적분을 위해 사다리꼴을 사용하는 사다리꼴 규칙은 Heun법과 비슷한데, 이는 구간의 양 끝점에서의 기울기를 평균한다. 둘 다 2차 방법으로, 전역 절단 오차는 간격 길이의 제곱과 비례한다.
* The Runge-Kutta method (RK4) parallels Simpson's rule for integration. Both emphasize the interval's midpoint, weighting it twice as heavily as the endpoints, and achieve fourth-order accuracy.<br>RK4 법은 심슨 적분과 유사하다. 둘 다 구간의 중점을 강조하여 끝점보다 두 배의 가중치를 둔다. 이렇게 하면 4차 정확도를 달성할 수 있다.

## References<br>참고문헌

* https://en.wikipedia.org/wiki/Euler_method#Global_truncation_error
