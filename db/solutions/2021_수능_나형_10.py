from sympy import symbols, summation, Eq, solve, Symbol
# Use symbolic sums consistent with the given constraints.
Sa = Symbol('Sa')  # sum a_k
Sb = Symbol('Sb')  # sum b_k
Sa_val = 8
Sb_val = 9
n = 5
# target expression: sum(2 a_k - b_k + 4) = 2*Sa - Sb + 4*n
expr = 2*Sa - Sb + 4*n
result = expr.subs({Sa: Sa_val, Sb: Sb_val})
CANDIDATE = 27
if Eq(result, CANDIDATE):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
