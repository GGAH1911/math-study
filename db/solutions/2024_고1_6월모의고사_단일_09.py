import sympy as sp

n = 5
# 부등식 |x-1| < n을 만족하는 정수 범위
# |x-1| < 5
# -5 < x-1 < 5
# -4 < x < 6

count = 0
valid_integers = []
for x_int in range(-10, 10):
    abs_expr = abs(x_int - 1)
    if abs_expr < n:
        count += 1
        valid_integers.append(x_int)

if count == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected 9 integers, got {count}: {valid_integers}')