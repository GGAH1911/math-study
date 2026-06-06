from sympy import symbols, Abs, solve

d = 5
a = lambda n: d * (n - 4)

# Verify condition 1: a_3 + a_5 = 0
cond1 = a(3) + a(5)
assert cond1 == 0, f'Condition 1 failed: {cond1}'

# Verify condition 2: sum of |a_k| + a_k for k=1 to 6
cond2 = sum(abs(a(k)) + a(k) for k in range(1, 7))
assert cond2 == 30, f'Condition 2 failed: {cond2}'

# Verify d is integer
assert isinstance(d, int), f'd must be integer: {d}'

# Compute a_9
a_9 = a(9)

if cond1 == 0 and cond2 == 30:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')