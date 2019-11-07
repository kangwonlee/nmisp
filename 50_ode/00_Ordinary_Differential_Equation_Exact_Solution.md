# 상미분 방정식의 엄밀해<br>An Exact Solution of an Ordinary Differential Equation



미분 방정식의 한 간단한 예는 다음과 같다.<br>A simple example of a differential equation is as follows.



$$
\begin{cases}
    \begin{align}
        a_0 \frac{d}{dt}x(t)+a_1 x(t)&=0 \\
        x(0)&=x_0 \\
    \end{align}
\end{cases}
$$



위 미분방정식의 해는 함수 $x(t)$ 이다.<br>
A solution for the differential equation above is the function $x(t)$.



어떤 미분방정식을 푼다는 것은, 해당 미분방정식을 만족하는 함수 $x(t)$를 찾는 것을 뜻한다.<br>
Solving for a differential equation means searching for a function $x(t)$ satisfying the differential equation.



처음에는 어떤 형태의 함수가 해당 미분 방정식을 만족시킬 것인지 잘 모를 수도 있겠지만 몇 가지 함수를 생각해 보자.<br>
At first, we may not be certain about which type of function may satisfy the equation above, but let's consider a few possible candiates.



## 다항식?<br>A polynomial?



다음과 같은 다항식이 만족시킬 수 있을까?<br>Is a polynomial as follows suitable?



$$
    x(t) = A_0 t^2 + A_1 t + A_2
$$



미분해 보자<br>Let's differentiate.



$$
    \frac{d}{dt}x(t) = 2 A_0 t + A_1
$$



각각 계수로 곱해보자.<br>Let's multiply with respective coefficients.



$$
\begin{cases}
    \begin{align}
        a_0 \frac{d}{dt}x(t) &= a_0 \left(2 A_0 t + A_1 \right)\\
        a_1 x(t)&=a_1 \left( A_0 t^2 + A_1 t + A_2 \right) \\
    \end{align}
\end{cases}
$$



등호의 오른쪽은 오른쪽 끼리, 등호의 왼쪽은 왼쪽 끼리 더해 보자.<br>Let's add each side respectively.



$$
\begin{align}
    a_1 x(t) + a_0\frac{d}{dt}x(t) &= a_1 \left( A_0 t^2 + A_1 t + A_2 \right) + a_0 \left(2 A_0 t + A_1 \right) \\
    & = a_1 A_0 t^2 + \left(2 a_0 A_0 + a_1 A_1\right) t + \left(a_0 A_1 + a_1 A_2\right)
\end{align}
$$



위에서<br>Remember



$$
a_0 \frac{d}{dt}x(t)+a_1 x(t)=0
$$



이었으므로 $t$가 어떤 값을 가지든 <br> thus for all $t$



$$
a_1 A_0 t^2 + \left(2 a_0 A_0 + a_1 A_1\right) t + \left(a_0 A_1 + a_1 A_2\right) = 0
$$



이어야 한다. <br> should be satisfied.



이러한 조건이 전혀 만족될 수 없는 것은 아닐 것이나, 일단은 좀 더 일반적으로 유용할 수 있어 보이는 경우를 살펴보도록 하자.<br>
Although this could be satisfied in some way or the other, however, for now let's take a look at a different case that seems more generally useful.



## 지수 함수?<br>Exponential Function?



아래와 같은 지수함수를 생각해 보자.<br>
Let's think about an exponential function as follows.



$$
    x(t) = A_0 e^{\lambda t}
$$



전과 마찬가지로, 미분하고 계수를 곱해 더해보자.<br>
As before, let's differentiate and add after multiplying coefficients.



$$
    \frac{d}{dt}x(t) = A_0 \lambda e^{\lambda t}
$$



$$
\begin{cases}
    \begin{align}
        a_0 \frac{d}{dt}x(t) &= a_0 \left(A_0 \lambda e^{\lambda t} \right)\\
        a_1 x(t)&=a_1 \left( A_0 e^{\lambda t} \right) \\
    \end{align}
\end{cases}
$$



$$
    a_0 \frac{d}{dt}x(t) + a_1 x(t) = a_0 \left(A_0 \lambda e^{\lambda t} \right) + a_1 \left( A_0 e^{\lambda t} \right) =0
$$



$t$가 어떤 값을 가지든 상관 없이 위 관계는 만족되어야한다.<br>For all $t$, the relationship above must be satisfied.



$A_0 e^{\lambda t}$ 에 관해 묶어 보자.<br>Let's factor out $A_0 e^{\lambda t}$.



$$
\begin{align}
a_0 \left(A_0 \lambda e^{\lambda t} \right) + a_1 \left( A_0 e^{\lambda t} \right) &= A_0 e^{\lambda t} a_0 \lambda  + A_0 e^{\lambda t} a_1 \\
&= A_0 e^{\lambda t} \left(a_0 \lambda  + a_1 \right)=0
\end{align}
$$



모든 $t$ 에 대해 위 식이 $0$이 되려면, $A_0=0$ 이거나 $a_0 \lambda + a_1 = 0$ 이어야 한다.<br>
To make the equation above to be $0$ for all $t$, either $A_0=0$ or $a_0 \lambda + a_1 = 0$.



$A_0=0$ 인 경우:<br>If $A_0=0$:



$$
    x(t)=0 \cdot e^{\lambda t} = 0
$$



$a_0 \lambda + a_1 = 0$ 인 경우:<br>If $a_0 \lambda + a_1 = 0$:



$$
\begin{align}
    a_0 \lambda + a_1 &= 0 \\
    \lambda &= -\frac{a_1}{a_0} \\
    x(t)&=A_0 e^{\lambda t}=A_0 e^{-\frac{a_1}{a_0} t}=A_0 exp\left(-\frac{a_1}{a_0} t\right)
\end{align}
$$



다항식의 경우와 비교해 보면 지수함수쪽이 조금 더 흥미있어 보일 수 있다.<br>Comparing with the polynomial, the exponential functions may seem somewhat more interesting.



## 초기 조건<br>Initial condition



그런데 $A_0$는 어떻게 정하는 것이 좋을까? 처음의 식으로 돌아가 보자.<br>However, what could be a good way to decide $A_0$? Let's go back to the first equation.



$$
\begin{cases}
    \begin{align}
        a_0 \frac{d}{dt}x(t)+a_1 x(t)&=0 \\
        x(0)&=x_0 \\
    \end{align}
\end{cases}
$$



따라서 $x(0)=x_0$ 였음을 이용해 보자. 여기서 $x_0$는 어떤 알려진 상수이다.<br>Thus let's use $x(0)=x_0$. Here, $x_0$ is a known constant.



$$
\begin{align}
    x(t)&=A_0 e^{-\frac{a_1}{a_0} t} \\
    x(0)&=A_0 e^{-\frac{a_1}{a_0}\cdot 0}=A_0 e^0=A_0 \cdot 1 = A_0=x_0 \\
    x(t)&=x_0 e^{-\frac{a_1}{a_0} t}
\end{align}
$$



이렇게 어떤 미분방정식의 엄밀해를 구할 수 있었다.<br>This way, we could find an exact solution of a differential equation.

