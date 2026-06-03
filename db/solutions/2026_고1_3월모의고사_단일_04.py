import sympy as sp
x = sp.Symbol('x')
# 원래 다항식
poly = (3*x - 1)*(x + 2) - x**2 - 8*x
poly_expanded = sp.expand(poly)
# a=1, b=-2로 인수분해
factored = (2*x + 1)*(x - 2)
factored_expanded = sp.expand(factored)
# 검증
if poly_expanded == factored_expanded:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')