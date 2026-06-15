from math import comb
# ₃H₅ = C(3+5-1,5)
CANDIDATE = 21
print('VERIFY_PASS' if comb(7,5) == CANDIDATE else 'VERIFY_FAIL')
