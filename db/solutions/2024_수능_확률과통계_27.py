from sympy import Rational, sqrt, solve, symbols, Eq, Abs

xbar, a = symbols('xbar a')

sigma = 5
n = 49
z = Rational(196, 100)

margin = z * sigma / sqrt(n)

eq1 = Eq(xbar - margin, a)
eq2 = Eq(xbar + margin, Rational(6, 5) * a)

sol = solve([eq1, eq2], [xbar, a])

xbar_val = sol[xbar]
a_val = sol[a]

lower = xbar_val - margin
upper = xbar_val + margin

cond1 = (xbar_val == Rational(154, 10))
cond2 = (a_val == 14)
cond3 = (upper == Rational(6, 5) * lower)

if cond1 and cond2 and cond3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'xbar={xbar_val}, a={a_val}, upper/lower={upper/lower}')
