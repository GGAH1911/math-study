import numpy as np

# 조건: 'x는 음이 아닌 실수이다' ⟺ x ≥ 0
# 정답: {x|x ≥ 0}

# 검증: 음이 아닌 = 0 이상
test_values = [-1, -0.5, 0, 0.5, 1, 100]
satisfies_condition = []

for x in test_values:
    # '음이 아닌 실수' 조건: x >= 0
    is_non_negative = x >= 0
    satisfies_condition.append(is_non_negative)

# 정답 {x|x >= 0}와 조건 만족 여부가 일치하는지 확인
all_match = True
for x, satisfies in zip(test_values, satisfies_condition):
    # x >= 0 조건
    expected = x >= 0
    if satisfies != expected:
        all_match = False
        break

if all_match:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')