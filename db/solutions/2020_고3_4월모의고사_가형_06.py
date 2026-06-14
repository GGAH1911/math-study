from sympy import symbols, limit, oo, S

# Given: lim a_n = 3
# Series sum(a_n + 2b_n - 7) converges => lim(a_n + 2b_n - 7) = 0
# So: 3 + 2 * lim(b_n) - 7 = 0

lim_a = S(3)
# Solve for lim_b_n
# 3 + 2*lim_b - 7 = 0
from sympy import solve, Symbol
lim_b = Symbol('lim_b')
result = solve(lim_a + 2*lim_b - 7, lim_b)
lim_b_val = result[0]

# Verify: the general term limit equals 0
general_term_limit = lim_a + 2*lim_b_val - 7
if lim_b_val == 2 and general_term_limit == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')