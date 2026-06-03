import math
from decimal import Decimal

# 방정식의 해들
solutions = [math.pi/4, 7*math.pi/4, 9*math.pi/4]

# 원래 방정식 검사: sqrt(2)*cos(x) - 1 = 0
for x in solutions:
    result = math.sqrt(2) * math.cos(x) - 1
    assert abs(result) < 1e-10, f'x={x}에서 검사 실패: {result}'

# 범위 확인
for x in solutions:
    assert 0 <= x <= 3*math.pi, f'x={x}가 범위를 벗어남'

# 합 검사
total = sum(solutions)
expected = 17*math.pi/4
assert abs(total - expected) < 1e-10, f'합 불일치: {total} vs {expected}'

print('VERIFY_PASS')