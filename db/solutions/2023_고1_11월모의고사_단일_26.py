import sympy as sp
from sympy import symbols, solve, simplify

t, a = symbols('t a', real=True)

# a = 23/4
a_val = sp.Rational(23, 4)

# 접선이 지나는 점의 t값: t^2 - 2at + 5a - 10 = 0
eq = t**2 - 2*a_val*t + 5*a_val - 10
sols = solve(eq, t)
t1, t2 = sols[0], sols[1]

# 기울기 계산
m1 = 2*t1 - 4
m2 = 2*t2 - 4

# 수직 조건 확인
product = simplify(m1 * m2)
print(f'기울기의 곱 m1*m2 = {product}')

# 기울기의 합
sum_m = simplify(m1 + m2)
print(f'기울기의 합 m1 + m2 = {sum_m}')

if product == -1 and sum_m == 15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')