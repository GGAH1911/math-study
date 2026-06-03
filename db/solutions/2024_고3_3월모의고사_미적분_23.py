from sympy import symbols, limit, oo, simplify
n = symbols('n', integer=True, positive=True)
expr = (2**(n+1) + 3**(n-1)) / (2**n - 3**n)
result = limit(expr, n, oo)
print('VERIFY_PASS' if simplify(result + 1/3) == 0 else 'VERIFY_FAIL')