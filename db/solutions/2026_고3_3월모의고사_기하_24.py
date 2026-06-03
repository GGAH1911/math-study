import sympy as sp
from sympy import sqrt

# 문제 조건
a = 3  # 단축의 반길이
b = 5  # 장축의 반길이 (y축)

# 타원 검증
# 방정식: x²/9 + y²/25 = 1
# 단축의 길이: 2*a = 2*3 = 6 ✓
assert 2*a == 6, "단축의 길이 검증 실패"

# 초점거리 계산
c = sqrt(b**2 - a**2)
assert c == 4, "초점거리 계산 실패"

# 두 초점 사이의 거리
distance = 2*c
assert distance == 8, "두 초점 사이의 거리 계산 실패"

print('VERIFY_PASS')