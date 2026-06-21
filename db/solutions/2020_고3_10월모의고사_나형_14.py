from sympy import symbols, solve, Abs
d = symbols('d', positive=True)
a = lambda k: 5 - 4*d + (k-1)*d
condition1 = a(5) - 5
condition2 = sum(Abs(2*a(k) - 10) for k in range(3, 8)) - 20
d_val = solve([condition1, condition2], d)[d]
a6 = 5 + d_val
print(f'VERIFY_PASS' if abs(float(d_val - 5/3)) < 1e-9 and abs(float(a6 - 20/3)) < 1e-9 else 'VERIFY_FAIL')