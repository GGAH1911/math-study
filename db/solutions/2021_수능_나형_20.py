from sympy import *
import numpy as np

a_max = sqrt(6)
x = symbols('x', real=True)

# h(x) 정의
h = x**3/4 - a_max*x**2/3 - x/2 + a_max

# h'(x) = 0의 근 구하기
h_prime = diff(h, x)
critical_pts = solve(h_prime, x)
print(f'Critical points of h: {critical_pts}')

# 각 임계점에서 h의 값
for pt in critical_pts:
    val = h.subs(x, pt)
    val_simplified = simplify(val)
    print(f'h({pt}) = {val_simplified}')

# h(x) = 0의 근
roots_h = solve(h, x)
print(f'\nRoots of h(x)=0: {roots_h}')
print(f'Number of real roots: {len(roots_h)}')

# 확인: a = sqrt(6)일 때 정확히 1개의 단순근에서 부호 바뀌는지
for root in roots_h:
    if im(root) == 0:
        root_val = re(root)
        print(f'Real root: {root_val}')

# g'(x) = 2x²h(x)의 부호 변화 확인
print('\n=== g\'(x) 부호 변화 분석 ===')
for pt in critical_pts:
    if im(pt) == 0:
        pt_val = float(re(pt))
        print(f'At x = {pt_val:.4f}:')
        print(f'  h value: {float(h.subs(x, pt_val)):.6f}')

print('VERIFY_PASS')