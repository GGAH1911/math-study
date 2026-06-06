import sympy as sp

# a_n = 11 - 3n
def a(n):
    return 11 - 3*n

# b_n 정의
def b(n):
    an = a(n)
    if an <= 0:
        return -2 * an
    else:
        return an

# 조건 (1) 검증: b_3 + b_5 = 2*b_4 + 6
left_1 = b(3) + b(5)
right_1 = 2 * b(4) + 6

# 조건 (2) 검증: b_4 + b_6 = 2*b_5
left_2 = b(4) + b(6)
right_2 = 2 * b(5)

# 합 계산
result = sum(b(k) for k in range(1, 11))

if left_1 == right_1 and left_2 == right_2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')

assert result == 155, f'Expected 155, got {result}'
assert left_1 == right_1, f'Condition 1 failed: {left_1} != {right_1}'
assert left_2 == right_2, f'Condition 2 failed: {left_2} != {right_2}'