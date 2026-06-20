from sympy import *
CANDIDATE = 9

# f(x) 정의
x = symbols('x')
f = x**4/4 + x**2/2 + 3

# 조건 1: f'(x) = x^3 + x 확인
f_prime = diff(f, x)
expected_derivative = x**3 + x
cond1 = simplify(f_prime - expected_derivative) == 0

# 조건 2: f(0) = 3 확인
f_at_0 = f.subs(x, 0)
cond2 = f_at_0 == 3

# 조건 3: f(2) = CANDIDATE 확인
f_at_2 = f.subs(x, 2)
cond3 = f_at_2 == CANDIDATE

if cond1 and cond2 and cond3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')