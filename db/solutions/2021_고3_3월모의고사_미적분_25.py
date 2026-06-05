from sympy import symbols, limit, oo, simplify

# a_1 = 2 로 검증
a1 = 2
n = symbols('n', integer=True, positive=True)

# a_n = a1^n
a_n = a1**n
a_n_plus_3 = a1**(n+3)

# 극한식
limit_expr = (3*a_n_plus_3 - 5) / (2*a_n + 1)
result = limit(limit_expr, n, oo)

if result == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')