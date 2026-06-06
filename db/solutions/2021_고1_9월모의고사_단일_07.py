from sympy import symbols, expand

x = symbols('x')

# 원래 주어진 식
original = (x**2 + 1)**2 + 3*(x**2 + 1) + 2

# a = 2, b = 3일 때의 인수분해 형태
factored = (x**2 + 2) * (x**2 + 3)

# 전개해서 비교
original_expanded = expand(original)
factored_expanded = expand(factored)

if original_expanded == factored_expanded:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')