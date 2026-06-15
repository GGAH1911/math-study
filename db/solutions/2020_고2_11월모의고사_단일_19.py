from sympy import symbols, diff, simplify

d = symbols('d', real=True)

# ∑a_k^2 = 15d^2 - 10d + 5
sum_sq = 15*d**2 - 10*d + 5

# ∑|a_k| = 7d - 1 (for d > 1)
sum_abs = 7*d - 1

# Objective function
S = sum_sq - 5*sum_abs
S = simplify(S)
print(f'S(d) = {S}')

# Find minimum
dS_dd = diff(S, d)
print(f'dS/dd = {dS_dd}')

d_opt = -dS_dd.coeff(d, 1) / (2 * dS_dd.coeff(d, 0) if dS_dd.coeff(d, 0) else dS_dd.coeff(d, 2))
from sympy import solve
d_opt = solve(dS_dd, d)[0]
print(f'd_opt = {d_opt}')

p = 1
q = d_opt
result = 7*(p + 2*q) - 1
result = simplify(result)
print(f'f(p+2q) = f({p}+2*{q}) = {result}')

if result == 27:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')