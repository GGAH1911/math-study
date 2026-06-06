from math import gcd
from functools import reduce

# 도형 경계 길이들
lengths = [90, 60, 150, 120, 72, 48]
max_a = reduce(gcd, lengths)

# 도형의 면적
original_area = 150 * 120
cut_area = 60 * 48
remaining_area = original_area - cut_area

# 정사각형 개수
num_squares = remaining_area // (max_a ** 2)

# 검증
assert max_a == 6, f'최대 한 변: {max_a}'
assert remaining_area == 15120, f'남은 넓이: {remaining_area}'
assert num_squares == 420, f'개수: {num_squares}'

print('VERIFY_PASS')