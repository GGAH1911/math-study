from sympy import symbols, expand

x = symbols('x')

# 원래 주어진 좌변과 우변 (문제에서의 식)
left = (2*x + 3)*(x - 2) + 8
right = 2*x*(x-2) + (-1)*(x-2) + 4*x  # a=2, b=-1, c=4 대입

# 전개
left_expanded = expand(left)
right_expanded = expand(right)

# 검증: 좌변과 우변이 같은지
if left_expanded == right_expanded:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')