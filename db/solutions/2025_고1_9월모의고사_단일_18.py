from sympy import symbols, solve, simplify, expand
x = symbols('x')
k = 15/4
eq = x**3 - 6*x**2 + (k+8)*x - 2*k
roots = solve(eq, x)
roots_sorted = sorted([float(r.evalf()) for r in roots])
alpha, beta, gamma = roots_sorted
print('Roots:', alpha, beta, gamma)
print('Vieta check:', abs(alpha + beta + gamma - 6) < 1e-9)
print('Condition check:', abs(2*alpha + beta - 2*gamma) < 1e-9)
print('Order check:', alpha < beta < gamma)
if all([abs(alpha + beta + gamma - 6) < 1e-9, abs(2*alpha + beta - 2*gamma) < 1e-9, alpha < beta < gamma]):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')