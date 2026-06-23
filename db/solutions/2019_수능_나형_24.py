import sympy as sp

CANDIDATE = 63

r = sp.Symbol('r', real=True, positive=True)

# 조건: r^3 = 3
eq = r**3 - 3
r_value = sp.solve(eq, r)[0]  # r = 3^(1/3)

# a_7 = 7 * r^6
a7 = 7 * r_value**6
a7_simplified = sp.simplify(a7)

# 검증
if a7_simplified == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')