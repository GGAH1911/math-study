from sympy import symbols, expand
x = symbols('x')
# 원래 식
lhs = (x**2 + 4)**2 - 3*x*(x**2 + 4) - 4*x**2
# 주어진 인수분해 형식으로 우변
a, b, c = -2, 1, 4
rhs = (x + a)**2 * (x**2 + b*x + c)
# 전개해서 비교
if expand(lhs - rhs) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')