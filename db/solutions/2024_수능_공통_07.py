from sympy import symbols, Rational, diff, solve
x = symbols('x')
f = Rational(1,3)*x**3 - 2*x**2 - 12*x + 4
fp = diff(f, x)
critical = solve(fp, x)
# alpha = local max, beta = local min
alpha = -2
beta = 6
assert alpha in critical and beta in critical, 'critical points mismatch'
fpp = diff(fp, x)
# second derivative test
assert fpp.subs(x, alpha) < 0, 'alpha should be local max'
assert fpp.subs(x, beta) > 0, 'beta should be local min'
result = beta - alpha
if result == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')