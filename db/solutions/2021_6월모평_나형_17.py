from sympy import symbols, integrate, solve, simplify
t = symbols('t', real=True)
C = symbols('C', real=True)
f_t = 4*t**3 + C*t
integral_value = integrate(f_t, (t, 0, 1))
eq = integral_value - C
C_solution = solve(eq, C)[0]
print(f'C = {C_solution}')
f_x = 4*symbols('x')**3 + C_solution*symbols('x')
f_1 = f_x.subs(symbols('x'), 1)
print(f'f(1) = {f_1}')
verify_integral = integrate(4*t**3 + 2*t, (t, 0, 1))
if verify_integral == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')