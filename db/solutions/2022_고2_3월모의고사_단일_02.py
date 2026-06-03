# 원래 조건: x > 1
# 부정: x ≤ 1

# 테스트: 부정이 올바른지 확인
# x > 1 일 때, x ≤ 1은 거짓
# x ≤ 1 일 때, x > 1은 거짓

test_cases = [
    (0.5, True),   # x=0.5: x≤1은 참, x>1은 거짓 ✓
    (1.0, True),   # x=1: x≤1은 참, x>1은 거짓 ✓
    (1.5, False),  # x=1.5: x≤1은 거짓, x>1은 참 ✓
    (2.0, False),  # x=2: x≤1은 거짓, x>1은 참 ✓
]

for x, should_satisfy_negation in test_cases:
    original = x > 1
    negation = x <= 1
    assert negation == should_satisfy_negation, f'Failed at x={x}'

print('VERIFY_PASS')