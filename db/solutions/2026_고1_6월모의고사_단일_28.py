from sympy import symbols, expand, div, sqrt

x = symbols('x')

# A(x) = (x-2)(x-3)(x-4)(x-5)
A = (x-2)*(x-3)*(x-4)*(x-5)
A_expanded = expand(A)

# 나누는 다항식
divisor = x**2 - 7*x - 1

# 다항식 나눗셈
quotient, remainder = div(A_expanded, divisor, x)

# 나머지 확인
if remainder == 143:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')