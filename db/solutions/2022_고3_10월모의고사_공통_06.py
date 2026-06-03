import sympy as sp
from sympy import sqrt, symbols, diff, simplify

a = 3 * sqrt(2)
x = symbols('x')
f = x**3 - 2*x**2 + 2*x + a

# 점 (1, f(1))의 좌표
f_at_1 = f.subs(x, 1)
print(f'f(1) = {f_at_1}')

# 접선의 기울기
f_prime = diff(f, x)
slope = f_prime.subs(x, 1)
print(f'f\'(1) = {slope}')

# 접선의 방정식: y - f(1) = slope * (x - 1)
# y = slope * x + (f(1) - slope)
# y = x + a
intercept = f_at_1 - slope
print(f'y축 절편 = {intercept}')
print(f'a = {a}')
print(f'일치 확인: {simplify(intercept - a) == 0}')

# P, Q 찾기
# P: x축과의 교점 (y=0) → 0 = x + a → x = -a
P_x = -a
P_y = 0
print(f'P = ({P_x}, {P_y})')

# Q: y축과의 교점 (x=0) → y = 0 + a = a
Q_x = 0
Q_y = a
print(f'Q = ({Q_x}, {Q_y})')

# PQ 거리
PQ_distance = sp.sqrt((P_x - Q_x)**2 + (P_y - Q_y)**2)
PQ_simplified = simplify(PQ_distance)
print(f'PQ = {PQ_simplified}')
print(f'PQ = 6 확인: {simplify(PQ_simplified - 6) == 0}')

if simplify(PQ_simplified - 6) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')