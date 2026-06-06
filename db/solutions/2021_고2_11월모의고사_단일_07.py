from sympy import symbols, solve, simplify
k = symbols('k', positive=True, real=True)
f = lambda x: x**3 + x**2 - 2*x
avg_rate = (f(k) - f(0)) / k
eq = avg_rate - 10
solutions = solve(eq, k)
print([sol for sol in solutions if sol > 0])
k_val = 3
avg_check = (f(k_val) - f(0)) / k_val
if abs(avg_check - 10) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')