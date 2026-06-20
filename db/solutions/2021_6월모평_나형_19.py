from sympy import *

x = symbols('x')
count = 0
valid_a = []

for a_val in range(-200, 201):
    expr = 2*x**3 + 6*x**2 + a_val
    roots = solve(expr, x)
    distinct_real = set()
    for r in roots:
        r_eval = complex(r.evalf())
        if abs(r_eval.imag) < 1e-8:
            rv = r_eval.real
            if -2 - 1e-9 <= rv <= 2 + 1e-9:
                distinct_real.add(round(rv, 7))
    if len(distinct_real) == 2:
        count += 1
        valid_a.append(a_val)

print(f'Valid a values: {valid_a}')
print(f'Count: {count}')
if count == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
