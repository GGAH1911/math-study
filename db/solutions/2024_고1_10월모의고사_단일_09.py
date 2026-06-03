from sympy import symbols, Eq, solve, Rational
a = symbols('a', real=True)
Ax, Ay = 3, 0
Bx, By = 0, a
m, n = 2, 3
Px = (m*Bx - n*Ax)/(m-n)
Py = (m*By - n*Ay)/(m-n)
eq = Eq((Px-3)**2 + (Py+8)**2, 36)
sols = solve(eq, a)
ans = 4
if any(abs(complex(s) - ans) < 1e-9 for s in sols):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
