from sympy import symbols, limit, oo, simplify
x = symbols('x', real=True, positive=True)
lower = x * (5*x - 1) / (x**2 + 1)
upper = x * (5*x + 2) / (x**2 + 1)
lim_lower = limit(lower, x, oo)
lim_upper = limit(upper, x, oo)
print(f'좌극한: {lim_lower}, 우극한: {lim_upper}')
if lim_lower == 5 and lim_upper == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')