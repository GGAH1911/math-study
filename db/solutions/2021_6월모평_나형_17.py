from sympy import symbols, integrate, solve, simplify

c = symbols('c', real=True)
t = symbols('t', real=True)

# c = integral of f(t) = 4t^3 + ct from 0 to 1
integral_value = integrate(4*t**3 + c*t, (t, 0, 1))
equation = c - integral_value
sol_c = solve(equation, c)
c_val = sol_c[0]

print(f'c = {c_val}')

# Now compute f(1)
f_at_1 = 4*(1)**3 + c_val*(1)
print(f'f(1) = {f_at_1}')

# Verify: check if f(x) = 4x^3 + cx with c=2 satisfies the original equation
x = symbols('x', real=True)
f = 4*x**3 + 2*x
integral_f = integrate(f, (x, 0, 1))
right_side = 4*x**3 + x*integral_f
verify = simplify(f - right_side)

if verify == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')