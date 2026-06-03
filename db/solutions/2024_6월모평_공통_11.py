import sympy as sp
from sympy import symbols, sqrt, limit, simplify, diff

t = symbols('t', real=True, positive=True)

# P = (t, t^2), Q = (1/t, 1)
P = (t, t**2)
Q = (1/t, 1)

# Distance PQ
PQ_squared = (1/t - t)**2 + (1 - t**2)**2
PQ = sqrt(PQ_squared)

# Simplify
PQ_simplified = sqrt((1 - t**2)**2 / t**2 + (1 - t**2)**2)
PQ_simplified = sqrt((1 - t**2)**2 * (1/t**2 + 1))
PQ_simplified = (1 - t**2) * sqrt(1 + t**2) / t  # for 0 < t < 1

# Calculate limit
limit_expr = (1 - t**2) * sqrt(1 + t**2) / (t * (1 - t))
limit_result = limit(limit_expr, t, 1, '-')

# Verify
if simplify(limit_result - 2*sqrt(2)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')