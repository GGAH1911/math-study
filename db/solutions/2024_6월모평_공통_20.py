import sympy as sp
from sympy import symbols, integrate, Abs

# Define variable
t, x = symbols('t x', real=True)
alpha = sp.Rational(6, 5)

# Define f(x)
f = lambda t_val: (t_val - alpha) * (t_val - 4)

# Define g(x) via numerical integration
g_expr = integrate(f(t), (t, 0, x))

# Substitute x = 9
f_9_value = (9 - alpha) * (9 - 4)
print(f'f(9) = {f_9_value}')

# Verify g(3) = 0
g_3_value = integrate(f(t), (t, 0, 3))
print(f'g(3) = {g_3_value}')

# Check f(4) = 0
f_4_value = f(4)
print(f'f(4) = {f_4_value}')

if f_9_value == 39 and g_3_value == 0 and f_4_value == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')