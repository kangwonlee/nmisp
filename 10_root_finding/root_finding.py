import pylab as py


def sequential(f, x_init, x_interval, epsilon, x_final):
    # result 의 초기값
    # Initial value for sqrt_10
    result = 'Not Found'

    # 일련의 x_i 값을 미리 준비한다
    # Prepare a series of x_i values in advance
    x_array = py.arange(x_init, x_final+x_interval*0.5, x_interval)

    # 몇번 반복했는지 측정해 보자
    # Let's count the number of iterations
    counter = 0

    # x_i 에 관한 반복문
    # x_i loop
    for x_i in x_array:
        # Evaluate the function
        y_i = f(x_i)
        
        counter += 1
        # Check if absolute value is smaller than epsilon
        if abs(y_i) < epsilon:
            result = x_i
            # found
            break

    # 반복 횟수
    # Number of iterations
    print('counter =', counter)

    return result


def bisection(f, x_lower, x_upper, epsilon):
    """
    이분법
    Bisection Method
    
    f : f(x) = 0 을 만족하는 x 를 찾고자 하는 함수 Function that we want to find x satisfying f(x) = 0
    x_lower : 초기 구간의 하한 Lower end of the initial interval
    x_upper : 초기 구간의 상한 Upper end of the initial interval
    epsilon : 희망하는 근의 정밀도 Desirable precision of the root
    """

    counter = 0
    
    # 간격이 epsilon 보다 더 길다면 계속 반복
    # Iterate while the interval is longer than epsilon
    while abs(x_upper - x_lower) > epsilon:
        # 구간을 둘로 나누는 x 를 계산
        # Calculate x bisecting the interval
        x_new = (x_upper + x_lower) * 0.5
        
        counter += 1
        
        # x_new 와 x_upper 사이에서 f(x)의 부호가 바뀐다면
        # If f(x)'s sign changes between x_new and x_upper
        if 0 > (f(x_upper) * f(x_new)):
            # 구간의 하한을 변경
            # Change the lower end of the interval
            x_lower = x_new

        # 그렇지 않고 x_lower 와 x_new 사이에서 f(x)의 부호가 바뀐다면
        # Else if f(x)'s sign changes between x_lower and x_new
        elif 0 > (f(x_lower) * f(x_new)):
            # 구간의 상한을 변경
            # Change the upper end of the interval
            x_upper = x_new

        # 둘 다 아니라면
        # If none of above
        else:
            # 무언가 잘못된 것으로 보임
            # Seems something is not right

            f_x_lower=f(x_lower)
            f_x_upper=f(x_upper)

            # 예외를 발생 시킴
            # Raise an exception
            raise ValueError(f'Something is not right:\nf({x_lower}) = {f_x_lower}\n'
                             f'f({x_upper}) = {f_x_upper}'
            )

    print('counter =', counter)
            
    return x_new


def newton_raphson(f, df_dx, x_initial, epsilon):
    """
    뉴튼 랩슨 법
    Newton Raphson Method
    
    f : f(x) = 0 을 만족하는 x 를 찾고자 하는 함수 Function that we want to find x satisfying f(x) = 0
    df_dx : f(x) 함수의 x 에 대한 미분 x-derivative of the function above
    x_initial : x의 초기값 Initial value of x
    epsilon : 희망하는 근의 정밀도 Desirable precision of the root
    """
    counter = 0
    
    # 변수 x_i 를 초기화
    # Initialize variable x_i
    x_i = x_initial

    # f(x_i) 의 절대값이 epsilon 보다 더 크다면 계속 반복
    # Iterate while the absolute value of f(x) is larger than epsilon
    while abs(f(x_i)) > epsilon:
        # x_i 지점에서의 접선의 기울기
        # Slope of the tangent at x_i
        slope = df_dx(x_i)
        
        assert abs(slope) > epsilon

        # 접선과 x축의 교점
        # Intersection of the tangent and the x axis
        x_i += - f(x_i) / slope

        counter += 1
    
    print('counter =', counter)
        
    return x_i

