from sympy import *

U = set(range(1, 21))
A = {3, 5, 6, 10, 12, 20}

# 1 not in A
assert 1 not in A

# Condition (나): P == Q
P = {x for x in U if x % 2 == 0 and (x // 2) in A}
Q = {x for x in U if x % 2 == 0 and x in A}
assert P == Q, f'P={P}, Q={Q}'

# Condition (가): exists x in U with x in A and x^2+1 in A
cond_ga = any(x in A and x**2 + 1 in A for x in U)
assert cond_ga, 'Condition (가) failed'

# Verify chain constraints (cond1 and cond2)
for a in A:
    if a <= 10:
        assert 2*a in A, f'Cond1 violated: {a} in A but {2*a} not in A'
for x in A:
    if x % 2 == 0:
        assert x // 2 in A, f'Cond2 violated: {x} in A but {x//2} not in A'

assert sum(A) == 56
print('VERIFY_PASS')
