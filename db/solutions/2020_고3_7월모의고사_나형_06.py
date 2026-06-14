from sympy import symbols, limit, solve, oo

a = symbols('a')
x = symbols('x')

# 함수 정의
def f_left(x_val):
    return -2*x_val + 1

def f_right(x_val, a_val):
    return x_val**2 - a_val*x_val + 4

# x=1에서의 좌극한 (x < 1에서)
left_limit = f_left(1)  # = -2(1) + 1 = -1

# x=1에서의 함수값 (x >= 1이므로 우측 함수 사용)
# f(1) = 1 - a + 4 = 5 - a
f_at_1 = 5 - a

# 연속성 조건: 좌극한 = 함수값
# -1 = 5 - a
a_value = solve(left_limit - f_at_1, a)[0]

# 검증: a = 6일 때 연속인지 확인
a_val = 6
left_result = f_left(1)
right_result = f_right(1, a_val)

if left_result == right_result:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')