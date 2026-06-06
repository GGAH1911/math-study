from sympy import symbols, diff, limit, solve

a, b, x = symbols('a b x')

# 주어진 함수 (a, b를 매개변수로)
def f_left(x_val, a_val, b_val):
    return x_val**3 - a_val*x_val + 2*b_val

def f_right(x_val, b_val):
    return -3*x_val + b_val

# 내 답: a=6, b=2
a_val, b_val = 6, 2

# 연속성 검증
f_left_at_1 = f_left(1, a_val, b_val)
f_right_at_1 = f_right(1, b_val)
assert f_left_at_1 == f_right_at_1, f"연속 실패: {f_left_at_1} != {f_right_at_1}"

# 미분가능성 검증
derivative_left_at_1 = 3*(1**2) - a_val
derivative_right_at_1 = -3
assert derivative_left_at_1 == derivative_right_at_1, f"미분가능 실패: {derivative_left_at_1} != {derivative_right_at_1}"

result = a_val * b_val
assert result == 12, f"곱셈 오류: {result}"

print('VERIFY_PASS')