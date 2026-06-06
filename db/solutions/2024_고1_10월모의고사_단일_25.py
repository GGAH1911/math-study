from sympy import symbols, expand, factor
x = symbols('x')
# 원래 식
original = (x**2 + 2*x) * (2*x**2 + 4*x + 5) + 3
# 제안한 인수분해
factored = (x + 1)**2 * (2*x**2 + 4*x + 3)
# 전개해서 비교
original_expanded = expand(original)
factored_expanded = expand(factored)
if original_expanded == factored_expanded:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')