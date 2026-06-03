from sympy import symbols, expand
x = symbols('x')
# 원래 식: 2x^2 + 9x + k (k=4)
original = 2*x**2 + 9*x + 4
# 인수분해 형태: (2x+a)(x+b) with a=1, b=4
factored = (2*x + 1)*(x + 4)
# 전개 확인
expanded = expand(factored)
if expanded == original:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')