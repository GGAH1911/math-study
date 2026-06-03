from sympy import *
x = symbols('x')

# 원래 식
original = (x**2 + x) * (x**2 + x + 2) - 8

# 우리 답: a=2, b=4
a, b = 2, 4
factored = (x - 1) * (x + a) * (x**2 + x + b)

# 전개해서 비교
original_expanded = expand(original)
factored_expanded = expand(factored)

# 두 식이 같은지 확인
if original_expanded == factored_expanded:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Original: {original_expanded}')
    print(f'Factored: {factored_expanded}')