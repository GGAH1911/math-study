import sympy as sp
x = sp.Symbol('x')
a_val = 2
b_val = 3

# 원래 다항식
original = x**4 - x**2 - 12

# 인수분해 형태
factored = (x - a_val) * (x + a_val) * (x**2 + b_val)
factored_expanded = sp.expand(factored)

# 두 식이 같은지 확인
if sp.simplify(original - factored_expanded) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')