import sympy as sp

CANDIDATE = 86

x = sp.Symbol('x')

# 원래 함수
f1 = 4*x**3 - 6*x + 4
f2 = 6*x - 1

# 정적분 계산
integral1 = sp.integrate(f1, (x, 1, 3))
integral2 = sp.integrate(f2, (x, 1, 3))

total = integral1 + integral2

if total == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')