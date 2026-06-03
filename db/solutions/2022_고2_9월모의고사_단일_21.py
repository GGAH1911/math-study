import sympy as sp

# Parameters
a_val = 12  # first term
d_val = 2   # common difference of {a_n}

def a_seq(n):
    return a_val + (n-1)*d_val

def b_seq(n):
    return a_val + (n-1)*(-2*d_val)

# Verify (가): |a_1| = |b_7|
assert abs(a_seq(1)) == abs(b_seq(7)), f'Cond(가) FAIL: |a1|={abs(a_seq(1))}, |b7|={abs(b_seq(7))}'

# Compute S_n
def S(n):
    return sum(abs(a_seq(k)) - abs(b_seq(k)) for k in range(1, n+1))

# Verify (나): S_n <= 108 for all n, and some S_p = 108
vals = [S(n) for n in range(1, 100)]
assert max(vals) == 108, f'max S_n = {max(vals)}'
assert 108 in vals, 'No p with S_p = 108'

# Find m = max n with S_n >= 0
m = max(n for n in range(1, 100) if S(n) >= 0)
assert m == 22, f'm = {m}, expected 22'

# Check a_m
a_m = a_seq(m)
if a_m == 54:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: a_{m} = {a_m}')
