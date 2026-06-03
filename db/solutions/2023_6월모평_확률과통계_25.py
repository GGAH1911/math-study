from fractions import Fraction
from math import comb

# 확률: 한 번에 이동할 확률 p = 2/3, 정지 q = 1/3
p = Fraction(2, 3)
q = Fraction(1, 3)

# 4번 시행 후 k번 이동했을 때 확률
prob = {}
for k in range(5):
    prob[k] = comb(4, k) * (p ** k) * (q ** (4 - k))

# 좌표가 2 이상일 확률 (좌표 = 이동 횟수)
result = prob[2] + prob[3] + prob[4]

print(f'P(좌표=0) = {prob[0]}')
print(f'P(좌표=1) = {prob[1]}')
print(f'P(좌표≥2) = {result}')
print(f'8/9와 비교: {result == Fraction(8, 9)}')

if result == Fraction(8, 9):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')