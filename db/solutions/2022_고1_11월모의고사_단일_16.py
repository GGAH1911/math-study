from sympy import symbols, expand

x = symbols('x')

# 원래 문제의 식
left_side = (x-1)*(x-4)*(x-5)*(x-8) + 36

# 우변 (우리의 답)
right_side = (x-2)**2 * (x-7)**2

# 전개 및 비교
left_expanded = expand(left_side)
right_expanded = expand(right_side)

difference = expand(left_expanded - right_expanded)

if difference == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')