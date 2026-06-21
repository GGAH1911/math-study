from sympy import symbols, diff, solve
t, k = symbols('t k')
x = t**3 + k*t**2 + k*t
v = diff(x, t)
a = diff(v, t)
k_val = solve(v.subs(t, 1), k)[0]
result = a.subs([(t, 2), (k, k_val)])
print('VERIFY_PASS' if result == 10 else f'VERIFY_FAIL: got {result}')