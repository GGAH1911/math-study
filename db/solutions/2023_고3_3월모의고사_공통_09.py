import sympy as sp
from sympy import symbols, diff, Abs, solve

x, p_val = symbols('x p_val', real=True)
p = 2

# 원래 함수
def g(x_val):
    return x_val**3 - 3*x_val**2 + p

# f(x) = |g(x)|
def f(x_val):
    return abs(g(x_val))

# 극댓값 조건 검증
f_0 = abs(g(0))
f_2 = abs(g(2))

print(f'f(0) = {f_0}')
print(f'f(2) = {f_2}')

if f_0 == f_2:
    print('조건 f(a)=f(b) 만족: PASS')
else:
    print(f'조건 불만족: {f_0} != {f_2}')

# 미분으로 극댓값 확인
g_prime = diff(x**3 - 3*x**2 + p, x)
print(f'g\'(x) = {g_prime}')

# x=0, x=2에서 g'(x)=0 확인
print(f'g\'(0) = {g_prime.subs(x, 0)}')
print(f'g\'(2) = {g_prime.subs(x, 2)}')

# 부호 확인: x=0 좌우에서 f'의 부호
test_left_0 = g_prime.subs(x, -0.1) * (1 if g(-0.1) > 0 else -1)
test_right_0 = g_prime.subs(x, 0.1) * (1 if g(0.1) > 0 else -1)
print(f'x=0 좌측: f\'(x) 부호 = {"양" if test_left_0 > 0 else "음"}')
print(f'x=0 우측: f\'(x) 부호 = {"양" if test_right_0 > 0 else "음"}')

# x=2 좌우에서 f'의 부호
test_left_2 = g_prime.subs(x, 1.9) * (1 if g(1.9) > 0 else -1)
test_right_2 = g_prime.subs(x, 2.1) * (1 if g(2.1) > 0 else -1)
print(f'x=2 좌측: f\'(x) 부호 = {"양" if test_left_2 > 0 else "음"}')
print(f'x=2 우측: f\'(x) 부호 = {"양" if test_right_2 > 0 else "음"}')

print('VERIFY_PASS')