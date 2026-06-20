from sympy import symbols, integrate, solve, Eq
t = symbols('t')
v = -4*t + 5
x = integrate(v, t)
C = symbols('C')
x_general = x + C
eq = Eq(x_general.subs(t, 3), 11)
C_val = solve(eq, C)[0]
x_final = x_general.subs(C, C_val)
result = x_final.subs(t, 0)
print('VERIFY_PASS' if result == 14 else 'VERIFY_FAIL')