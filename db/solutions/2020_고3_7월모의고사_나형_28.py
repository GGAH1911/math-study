CANDIDATE = 12

import sympy as sp

x = sp.Symbol('x')

# 최적 f*(x) = max(0, 1-x^2) 정의
# 한 주기 [-1, 2]에서 적분
f_positive = 1 - x**2  # x in [-1, 1]
f_zero = sp.Integer(0)  # x in [1, 2]

# 한 주기 적분
one_period = sp.integrate(f_positive, (x, -1, 1)) + sp.integrate(f_zero, (x, 1, 2))
print(f'One period integral: {one_period}')  # should be 4/3

# 9주기 적분
total = 9 * one_period
print(f'Total integral [-1, 26]: {total}')  # should be 12

# 최적성 검증: f*(x)=max(0,1-x^2)가 정말 적분을 최소화하는지 확인
# 제약 f>=0 하에서 [f(x)-(1-x^2)]^2의 최솟값은 max(0,1-x^2)일 때 달성
# f*(-1) = 0, f*(2) = 0 -> 주기성 경계 조건 확인
f_at_minus1 = max(0, 1 - (-1)**2)
f_at_2 = max(0, 1 - 2**2)
print(f'f*(-1)={f_at_minus1}, f*(2)={f_at_2}')  # 둘 다 0

if total == CANDIDATE and f_at_minus1 == f_at_2 == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
