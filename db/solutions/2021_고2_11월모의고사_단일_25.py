import sympy as sp
k = sp.Symbol('k')
a = 2
# 원래 조건: sum(k^2 - ak) = 275
sum_k2 = sum([i**2 for i in range(1, 11)])
sum_k = sum([i for i in range(1, 11)])
result = sum_k2 - a * sum_k
if result == 275:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')