# Comparison with Numerical Integration<br>수치적분과의 비교


* Let's consider a differential equation of the following form, which represents Newton's second law of motion:<br>다음 미분 방정식을 생각해 보자. 이것은 뉴튼의 두번째 법칙을 나타낸 것이다.

$$
    \frac{d^2x}{dt^2}+0 \cdot \frac{dx}{dt} + 0 \cdot x = \frac{1}{m}f(t)
$$

* This equation tells us that the acceleration of an object is proportional to the net force acting on it.<br>이 식에 따르면, 어떤 물체의 가속도는 그 물체에 가해지는 합력에 비례한다는 것이다.
* To find the object's position $x(t)$, we need to integrate the acceleration twice.<br>해당 물체의 위치 $x(t)$를 찾기 위해서는 가속도를 두 번 적분해야 한다.
* This reveals a deep connection between solving differential equations and numerical integration.<br>이는 미분방정식을 푸는 과정과 수치적분 사이에 깊은 연관성이 있다는 것을 보여준다.

* The following compares numerical integration methods with their corresponding ODE solvers:<br>아래는 수치적분 방법과 그에 대응하는 미분방정식 해법을 비교한 것이다.
* Both kinds of method work by **measuring at several points and taking a weighted average**. The pairs below use the **same set of weights**.<br>두 종류의 방법 모두 **여러 점에서 측정한 다음 가중 평균을 취하는** 방식으로 동작한다. 아래 짝지어진 방법들은 **같은 가중치**를 사용한다.

### Rectangle 직사각형 ↔ Euler 오일러 — 1 sample 한 점 측정

* Measure once at the start of the step. Use that single value for the whole step.<br>구간의 시작점에서 한 번만 측정한 다음, 그 값을 구간 전체에 사용한다.

$$F_k = f(x_k)\cdot \Delta x$$

$$x_{k+1} = x_{k} + \Delta t \cdot f(x_k, t_k)$$

### Trapezoid 사다리꼴 ↔ Heun 훈 — 2 samples 양 끝 점 측정

* Measure at both endpoints; average them with equal weight $\frac{1}{2}, \frac{1}{2}$.<br>양 끝점에서 측정한 다음, 같은 가중치 $\frac{1}{2}, \frac{1}{2}$로 평균을 낸다.

$$F_k = \frac{\Delta x}{2}\left[f(x_k) + f(x_{k+1})\right]$$

$$x_{k+1} = x_{k} + \frac{\Delta t}{2}\left[f(x_k, t_k) + f(\hat{x}_{k+1}, t_{k+1})\right]$$

### Simpson 심프슨 ↔ Runge-Kutta 룽게-쿠타 — 3 sampling points (middle counted twice) 가운데를 두 번 세는 3 점 측정

* Measure at start, middle, end. The **middle measurement counts 4 times more** than the endpoints — the weights are $\frac{1}{6}, \frac{4}{6}, \frac{1}{6}$.<br>시작 · 가운데 · 끝에서 측정하되, **가운데 측정값은 끝 점들보다 4배 더 무겁게** 센다. 가중치는 $\frac{1}{6}, \frac{4}{6}, \frac{1}{6}$이다.

$$F_k = \frac{\Delta x}{6}\left[f(x_{k}) + 4 \cdot f(x_{k+1}) + f(x_{k+2})\right]$$

* RK4 has **four** slope measurements: 1 at the start, 2 at the middle, 1 at the end — weighted $\frac{1}{6}, \frac{2}{6}, \frac{2}{6}, \frac{1}{6}$.<br>RK4 는 **네 번** 기울기를 측정한다 : 시작에서 1번, 가운데에서 2번, 끝에서 1번 — 가중치는 $\frac{1}{6}, \frac{2}{6}, \frac{2}{6}, \frac{1}{6}$ 이다.
* When the **two middle slopes turn out to be the same**, the two middle terms combine: $\frac{2}{6} + \frac{2}{6} = \frac{4}{6}$. The pattern $\frac{1}{6}, \frac{4}{6}, \frac{1}{6}$ becomes exactly Simpson's rule.<br>**가운데에서 잰 두 기울기 값이 같아지면**, 두 가운데 항이 합쳐져 $\frac{2}{6} + \frac{2}{6} = \frac{4}{6}$ 이 된다. 그러면 $\frac{1}{6}, \frac{4}{6}, \frac{1}{6}$ 패턴이 나타나 Simpson 규칙과 정확히 같아진다.

$$x_{k+1} = x_{k} + \frac{\Delta t}{6} \left[f(x_k, t_k) + 2 f(\hat{x}_{k+\frac{1}{2}}, t_{k+\frac{1}{2}})_1+ 2 f(\hat{x}_{k+\frac{1}{2}}, t_{k+\frac{1}{2}})_2 + f(\hat{x}_{k+1}, t_{k+1})\right]$$

* Both kinds of method approximate the answer with a **weighted average of measurements**. Integration averages function *values*; ODE solvers average *slopes*.<br>두 종류의 방법 모두 **측정값들의 가중 평균**으로 답을 근사한다. 적분에서는 함수 *값*을, 상미분방정식 해법에서는 *기울기*를 평균한다.
* More measurement points → smaller error, but more computation per step. Choose the trade-off that fits the problem.<br>측정 점이 많아질수록 오차는 작아지나 한 단계 당 계산량은 늘어난다. 문제에 맞는 절충점을 고르면 된다.
* The Rectangle/Euler pair: one measurement per step → simple, but error builds up quickly. Good when you just want a rough picture.<br>직사각형/오일러 짝 : 한 단계에 한 번 측정 → 간단하지만 오차가 빠르게 쌓인다. 대략적인 모양만 보고 싶을 때 좋다.
* The Trapezoid/Heun pair: two measurements per step → much smaller error for only a little more work.<br>사다리꼴/Heun 짝 : 한 단계에 두 번 측정 → 약간의 추가 계산으로 오차가 훨씬 작아진다.
* The Simpson/RK4 pair: three sampling points, with the middle counted four times → the standard "default" pick for science and engineering when accuracy matters.<br>Simpson/RK4 짝 : 세 군데서 측정하되 가운데를 4배로 셈 → 정확도가 필요한 과학·공학 문제에서 표준으로 사용되는 방법이다.

## See also<br>관련 문서

* [`30_num_int/`](../30_num_int/) — the same comparison from the integration side (Rectangle / Trapezoid / Simpson explained from first principles).<br>적분 쪽에서 같은 비교를 다룬다 (직사각형 / 사다리꼴 / Simpson 규칙을 처음부터).

## References<br>참고문헌

* https://en.wikipedia.org/wiki/Euler_method#Global_truncation_error
* https://en.wikipedia.org/wiki/Simpson%27s_rule
* https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods
