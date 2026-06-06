import math
from fractions import Fraction

# 전체 경우의 수
total = math.factorial(9)

# 유리한 경우: A의 바로 양옆에 각각 숫자가 놓이는 경우
# A의 위치: 2~8 (7가지)
# A 왼쪽에 올 숫자: 4가지
# A 오른쪽에 올 숫자: 3가지
# 남은 6개 카드를 6개 위치에 배열: 6!
favorable = 7 * 4 * 3 * math.factorial(6)

# 확률
prob = Fraction(favorable, total)
print(f'확률: {prob}')
print(f'확률 값: {float(prob)}')
print(f'1/6 확인: {prob == Fraction(1, 6)}')
if prob == Fraction(1, 6):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')