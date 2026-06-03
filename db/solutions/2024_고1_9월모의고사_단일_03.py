from sympy import symbols, expand, simplify

x = symbols('x')

# 주어진 조건: a=3, b=4
a_val = 3
b_val = 4

# 좌변: x^2 + ax + b
left = x**2 + a_val*x + b_val

# 우변: x(x+3) + 4
right = x*(x + 3) + 4

# 전개
right_expanded = expand(right)
left_expanded = expand(left)

# 차이 계산
difference = simplify(left_expanded - right_expanded)

# 검증
if difference == 0:
    # 여러 x값으로도 확인
    for test_x in [-2, -1, 0, 1, 2, 3]:
        left_val = left.subs(x, test_x)
        right_val = right.subs(x, test_x)
        assert left_val == right_val, f'Failed at x={test_x}'
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')