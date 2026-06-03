from sympy import symbols, solve, Rational, simplify

# 주어진 조건으로부터 얻은 r=-1/2 검증
r = Rational(-1, 2)
a1 = 8 * r

# 수열 항 계산
a2 = a1 * r
a3 = a1 * r**2
a5 = a1 * r**4
a8 = a1 * r**7

# 조건 1: a3 * a5 = 8 * a8
cond1_lhs = a3 * a5
cond1_rhs = 8 * a8
cond1_check = simplify(cond1_lhs - cond1_rhs) == 0

# 조건 2: a1 + |a2| + |2*a3| = 0
cond2_lhs = a1 + abs(a2) + abs(2*a3)
cond2_check = simplify(cond2_lhs) == 0

if cond1_check and cond2_check:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')