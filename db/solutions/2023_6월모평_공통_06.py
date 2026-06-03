import sympy as sp
from sympy import Abs

# 구간별 f(x) 정의
x = sp.Symbol('x', real=True)
a_val = 2
b_val = sp.Rational(5, 3)

def f(x_val):
    if x_val < -1:
        return x_val + a_val
    elif -1 <= x_val < 3:
        return x_val
    else:  # x >= 3
        return b_val * x_val - 2

# 주요 불연속점(f의)에서 |f|의 연속성 확인
# x = -1에서
f_left_minus1 = -1 + a_val  # = 1
f_right_minus1 = -1  # = -1
abs_left = abs(f_left_minus1)  # 1
abs_right = abs(f_right_minus1)  # 1
print(f'x=-1에서: |f(x)| 좌극한={abs_left}, 우극한={abs_right}', 'PASS' if abs_left == abs_right else 'FAIL')

# x = 3에서
f_left_3 = 3
f_right_3 = b_val * 3 - 2  # = 5 - 2 = 3
abs_left_3 = abs(f_left_3)  # 3
abs_right_3 = abs(f_right_3)  # 3
print(f'x=3에서: |f(x)| 좌극한={abs_left_3}, 우극한={abs_right_3}', 'PASS' if abs_left_3 == abs_right_3 else 'FAIL')

# x = -2에서 (a=2일 때 f의 부호가 바뀌는 점)
f_at_minus2 = -2 + a_val  # = 0
f_left_minus2 = -2 + a_val - 0.01  # x < -2
f_right_minus2 = -2 + a_val + 0.01  # -2 < x < -1
abs_left_minus2 = abs(-2.01 + a_val)
abs_right_minus2 = abs(-1.99 + a_val)
print(f'x=-2에서: |f(x)| 좌극한≈{abs_left_minus2:.4f}, 우극한≈{abs_right_minus2:.4f}, f(-2)={abs(f_at_minus2)}', 'PASS' if abs(f_at_minus2) == 0 else 'FAIL')

# 최종 답 검증
answer = a_val + b_val
print(f'\n최종: a + b = {a_val} + {b_val} = {answer}')
if answer == sp.Rational(11, 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')