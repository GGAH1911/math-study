import sympy as sp

# 원래 함수
h = sp.Symbol('h')
f = lambda x: x**3 - 3*x**2 + x

# 극한값 계산
result = sp.limit((f(3 + h) - f(3)) / (2 * h), h, 0)

# 검증
if result == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')