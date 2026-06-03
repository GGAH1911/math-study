from sympy import symbols, Abs, solve, S
x = symbols('x', real=True)
sol = solve(Abs(2*x-3) < 5, x)
# sol should be the interval (-1, 4)
a, b = -1, 4
ans = a + b
# Verify by checking boundary points satisfy |2x-3| = 5 and interior satisfies < 5
lhs_a = abs(2*a - 3)
lhs_b = abs(2*b - 3)
mid = (a+b)/2
lhs_mid = abs(2*mid - 3)
if lhs_a == 5 and lhs_b == 5 and lhs_mid < 5 and ans == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
