from sympy import symbols, solve, sqrt
b_sq = 20
a_sq = 16
c_sq = a_sq + b_sq
c = sqrt(c_sq)
y_P = b_sq / 4
PF_distance = y_P
assert PF_distance == 5, f'Expected PF=5, got {PF_distance}'
print('VERIFY_PASS')