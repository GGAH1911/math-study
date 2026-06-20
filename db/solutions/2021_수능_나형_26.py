import sympy as sp
from sympy import sqrt, limit, oo

CANDIDATE = 6

x = sp.Symbol('x')
a = 7  # 우리가 구한 a
b = -1  # 우리가 구한 b

# x <= 1일 때 함수
f_left = -3*x + a

# x > 1일 때 함수
f_right = (x + b) / (sqrt(x + 3) - 2)

# x = 1에서의 좌극한
left_limit = f_left.subs(x, 1)
print(f'좌극한 (x=1-): {left_limit}')

# x = 1에서의 우극한
right_limit = limit(f_right, x, 1, '+')
print(f'우극한 (x=1+): {right_limit}')

# 연속성 검증
if left_limit == right_limit == 4:
    print(f'x=1에서 연속: {left_limit}')
    if left_limit + 0 == right_limit:  # 함수값이 -3+a
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print(f'연속 조건 불만족')
    print('VERIFY_FAIL')

# 최종 검증: CANDIDATE == a + b
if CANDIDATE == a + b:
    print(f'CANDIDATE = {CANDIDATE} = a + b = {a + b}')
else:
    print('VERIFY_FAIL')