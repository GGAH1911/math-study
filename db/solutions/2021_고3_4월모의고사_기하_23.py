from sympy import symbols, simplify, Matrix
a, b, m, n = symbols('a b m n')
# 좌변: (2*a - m*b) - (n*a - 4*b)
lhs_a_coeff = 2 - n
lhs_b_coeff = -m + 4
# 우변: a - b
rhs_a_coeff = 1
rhs_b_coeff = -1
# m=5, n=1로 검증
m_val, n_val = 5, 1
lhs_a_check = lhs_a_coeff.subs(n, n_val)
lhs_b_check = lhs_b_coeff.subs(m, m_val)
if lhs_a_check == rhs_a_coeff and lhs_b_check == rhs_b_coeff:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')