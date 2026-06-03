from sympy import symbols, solve, Rational, simplify

x = symbols('x')
roots = solve(x**2 - 2*x + 5, x)
alpha, beta = roots[0], roots[1]
result = simplify(1/alpha + 1/beta)
expected = Rational(2, 5)
if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}, expected {expected}')
