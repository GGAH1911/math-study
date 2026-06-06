import sympy as sp
from sympy import symbols, solve, sqrt

x, a = symbols('x a', real=True, positive=True)

# 원래 함수
f = lambda x_val: x_val**3 + a*x_val
f_prime = lambda x_val: 3*x_val**2 + a

# 평균변화율 (x=1 to x=3)
average_rate = (f(3) - f(1)) / (3 - 1)
average_rate_simplified = sp.simplify(average_rate)

# f'(a)
f_prime_a = f_prime(a)

# 조건: 평균변화율 = f'(a)
equation = sp.Eq(average_rate_simplified, f_prime_a)
solution_a_squared = sp.solve(equation, a**2)

if solution_a_squared:
    a_squared_value = solution_a_squared[0]
    result = 3 * a_squared_value
    if result == 13:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: got {result}')
else:
    print('VERIFY_FAIL')