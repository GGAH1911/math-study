import sympy as sp
from sympy import symbols, integrate, Abs

k_val = sp.Rational(4, 3)
x = symbols('x')
f = k_val * x * (x - 2) * (x - 3)

# 영역 A: 0부터 2까지
A = integrate(f, (x, 0, 2))

# 영역 B: 2부터 3까지 (f가 음수이므로 절댓값)
B = -integrate(f, (x, 2, 3))

# 조건 확인
result = A - B
if result == 3:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: A-B={result}')