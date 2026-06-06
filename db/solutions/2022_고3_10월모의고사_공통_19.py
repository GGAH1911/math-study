import sympy as sp
from sympy import symbols, integrate, diff

t, k = symbols('t k', real=True, positive=True)
v = 4*t**3 - 48*t
a = diff(v, t)

# k 값 구하기: a(k) = 0
k_val = sp.solve(a.subs(t, k), k)[0]
assert k_val == 2, f'k should be 2, got {k_val}'

# 0부터 2까지의 이동 거리
# v(t)가 (0,2] 구간에서 항상 음수인지 확인
v_at_1 = v.subs(t, 1)
assert v_at_1 < 0, f'v(1) should be negative, got {v_at_1}'

# 적분 계산
integral_result = integrate(v, (t, 0, 2))
distance = abs(integral_result)
assert distance == 80, f'distance should be 80, got {distance}'
print('VERIFY_PASS')