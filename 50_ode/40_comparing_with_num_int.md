# Comparison with Numerical Integration<br>수치적분과의 비교



Let's think about a differential equation of following form.<br>다음 미분 방정식을 생각해 보자.

$$
    \frac{d^2x}{dt^2}+0 \cdot \frac{dx}{dt} + 0 \cdot x = \frac{1}{m}f(t)
$$

In fact, the equation above is the Newton's second law of motion, and we can solve it by integrating the right side twice.<br>실은 위 식은 뉴턴의 2번째 운동법칙으로 그 해는 우변을 두번 적분한 것이다.


Considering this example, solving for a differential equation and integration might be somewhat related.<br>이 예를 생각해 보면, 미분방정식을 푸는 과정과 적분은 무언가 통하는 점이 있을 수 있다.

|  order  | Numerical Integration       | method | ODE Solver                    |
|:---------:|:--------------------------------:|:--------:|:------------------------------------------------:|
| 0th order | $$ F_k = f(x_k)\cdot \Delta x $$ |  Euler   | $$ x_{k+1} = x_{k} + \Delta t \cdot f(x_k, t_k) $$ |
| 1st order | $$ F_k = \frac{\Delta x}{2}\left[f(x_k) + f(x_{k+1})\right] $$ |  Heun   | $$ x_{k+1} = x_{k} + \frac{\Delta t}{2} \left[f(x_k, t_k) + f(\hat{x}_{k+1}, t_{k+1})\right] $$ |
| 2nd order | $$ F_k = \frac{\Delta x}{6}\left[f(x_k) + 4 \cdot f(x_{k+1}) + f(x_{k+2})\right] $$ |  Runge-Kutta   | $$ x_{k+1} = x_{k} + \frac{\Delta t}{6} \left[f(x_k, t_k) + 2 f(\hat{x}_{k+\frac{1}{2}}, t_{k+\frac{1}{2}})_1+ 2 f(\hat{x}_{k+\frac{1}{2}}, t_{k+\frac{1}{2}})_2 + f(\hat{x}_{k+1}, t_{k+1})\right] $$ |
