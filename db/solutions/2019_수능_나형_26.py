CANDIDATE = 2

import sympy as sp

# 문제: y=sqrt(x+3)과 y=sqrt(1-x)+k가 만날 조건에서 k의 최댓값
# 만나는 조건: sqrt(x+3) = sqrt(1-x) + k
# k = sqrt(x+3) - sqrt(1-x) 의 최댓값을 구함
# 정의역: x in [-3, 1]

x = sp.Symbol('x', real=True)
f = sp.sqrt(x + 3) - sp.sqrt(1 - x)

# 도함수
f_prime = sp.diff(f, x)

# 경계값 계산
f_at_minus3 = f.subs(x, -3)
f_at_1 = f.subs(x, 1)

print(f'f(-3) = {float(f_at_minus3)}')
print(f'f(1) = {float(f_at_1)}')

# f'(x) > 0 for all x in (-3, 1) 이므로 f는 순증가
# 최댓값은 x=1에서
max_k_value = float(f_at_1.evalf())

if abs(max_k_value - CANDIDATE) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')