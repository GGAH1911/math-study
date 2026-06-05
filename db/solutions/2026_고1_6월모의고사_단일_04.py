import sympy as sp
x = sp.Symbol('x')
# 원래 다항식
original = x**3 + 2*x**2 + x + 2
# 내 답: a=1, b=2
a, b = 1, 2
factored = (x**2 + a) * (x + b)
expanded = sp.expand(factored)
if sp.simplify(original - expanded) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')