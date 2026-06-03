import sympy as sp
a = 48
r = -1/2
a_vals = [a * r**(k-1) for k in range(1, 6)]
assert a_vals[2] + 2*a_vals[3] == 0, f'Condition 1 failed: {a_vals[2]} + 2*{a_vals[3]}'
assert sum(a_vals) == 33, f'Condition 2 failed: sum = {sum(a_vals)}'
print('VERIFY_PASS')