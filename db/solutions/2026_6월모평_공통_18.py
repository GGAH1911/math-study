import sympy as sp
k = sp.Symbol('k')
# 원래 문제식 검증: k=1부터 6까지의 합
result = sum(k**2 + 2*k for k in range(1, 7))
print('VERIFY_PASS' if result == 133 else 'VERIFY_FAIL')