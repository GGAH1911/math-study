from sympy import symbols, expand, simplify
t = symbols('t', real=True)
l_squared = (2*t - (-1))**2 + (-3 - 2*t)**2
l_squared_expanded = expand(l_squared)
min_val = 2
t_at_min = -1
result = l_squared_expanded.subs(t, t_at_min)
if result == min_val:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')