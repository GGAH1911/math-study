import sympy as sp
# ₆P₂ - ₆C₂
n, r = 6, 2
CANDIDATE = 15
val = sp.ff(n, r) - sp.binomial(n, r)   # 순열 - 조합
print('VERIFY_PASS' if val == CANDIDATE else 'VERIFY_FAIL')
