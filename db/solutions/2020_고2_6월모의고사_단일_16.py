import sympy as sp

a_val = 1/sp.sqrt(2)
b_val = sp.sqrt(2)

log2_a = sp.log(a_val, 2)
log2_b = sp.log(b_val, 2)

# Condition 1: ab = 1
assert sp.simplify(a_val * b_val - 1) == 0, 'Cond1 fail'

# Condition 2: external division 1:2 on y-axis => 2a - b = 0
assert sp.simplify(2*a_val - b_val) == 0, 'Cond2 fail'

dx = b_val - a_val
dy = log2_b - log2_a
length = sp.sqrt(dx**2 + dy**2)
length_s = sp.simplify(length)

expected = sp.sqrt(6) / 2
if sp.simplify(length_s - expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {length_s}, expected {expected}')