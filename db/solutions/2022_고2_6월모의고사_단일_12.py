import math

# 원래 부등식 검증
def verify_inequality(x):
    if x + 5 <= 0:
        return False
    lhs = math.log(x + 5, 3)
    rhs = 8 * math.log(2, 9)
    return lhs < rhs

# 경계값 검증
min_val = -4
max_val = 10

# 최솟값 -4 검증
assert verify_inequality(min_val), f'min {min_val} fails'
assert not verify_inequality(min_val - 1), f'{min_val - 1} should not satisfy'

# 최댓값 10 검증
assert verify_inequality(max_val), f'max {max_val} fails'
assert not verify_inequality(max_val + 1), f'{max_val + 1} should not satisfy'

# 합 검증
answer_sum = min_val + max_val
assert answer_sum == 6, f'sum {answer_sum} != 6'

print('VERIFY_PASS')