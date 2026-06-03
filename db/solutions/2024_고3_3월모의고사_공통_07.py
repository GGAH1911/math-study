from sympy import symbols, diff, solve, Rational, factor
import numpy as np

x = symbols('x')
f = Rational(1,3)*x**3 - 2*x**2 - 5*x + 1
fp = diff(f, x)

# 감소 구간 확인: f'(x) <= 0 인 구간이 [-1, 5]
critical = sorted(solve(fp, x))
assert critical == [-1, 5], f'critical points wrong: {critical}'

# [-1, 5]에서 f' <= 0 검증
x_vals = np.linspace(-1, 5, 10000)
fp_vals = np.array([float(fp.subs(x, xi)) for xi in x_vals])
if all(v <= 1e-9 for v in fp_vals) and (5 - (-1)) == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
