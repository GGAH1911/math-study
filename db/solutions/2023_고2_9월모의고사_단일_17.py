from sympy import symbols, solve, diff
d = symbols('d', positive=True, real=True)
a1 = 1 / d
a4 = a1 + 3*d
a6 = a1 + 5*d
a3 = a1 + 2*d
a22 = a1 + 21*d
a7 = a1 + 6*d
a8 = a1 + 7*d

# 조건 (나) 검증
lhs = a3 * a22
rhs = a7 * a8 + 10
cond_na = lhs - rhs
cond_na_simplified = cond_na.simplify()
if cond_na_simplified == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')