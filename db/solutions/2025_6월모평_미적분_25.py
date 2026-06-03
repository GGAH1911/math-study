from sympy import limit, oo, symbols, Rational

# 급수 수렴 필요조건: 일반항 -> 0
# lim a_n = lim (3n^2 - n) / (2n^2 + 1) = 3/2
n = symbols('n', positive=True, integer=True)
expr = (3*n**2 - n) / (2*n**2 + 1)
lim_an = limit(expr, n, oo)

# lim (a_n^2 + 2*a_n)
result = lim_an**2 + 2*lim_an
expected = Rational(21, 4)

if result == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}, expected {expected}')
