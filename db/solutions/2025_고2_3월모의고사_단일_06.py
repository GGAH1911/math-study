from sympy import symbols, solve, discriminant, Poly
a = symbols('a', real=True, positive=True)
x = symbols('x', real=True)
eq = x**2 + (2-2*a)*x + (a+1)
disc = discriminant(Poly(eq, x), x)
solution = solve(disc, a)
positive_sol = [s for s in solution if s > 0]
print('VERIFY_PASS' if positive_sol == [3] else 'VERIFY_FAIL')