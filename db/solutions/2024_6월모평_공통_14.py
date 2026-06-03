import sympy as sp
t = sp.Symbol('t')
a_val = 1
v = -t*(t-1)*(t-a_val)*(t-2*a_val)
integral_result = sp.integrate(v, (t, 0, 2))
print(f'Integral result: {integral_result}')
print(f'Absolute value: {abs(integral_result)}')
if abs(integral_result - sp.Rational(4,15)) < 1e-10 or abs(integral_result + sp.Rational(4,15)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')