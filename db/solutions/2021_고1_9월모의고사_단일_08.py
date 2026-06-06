import math

# 원래 문제: |2x - 1| ≤ 5를 만족하는 정수 x의 개수
count = 0
valid_integers = []

for x in range(-10, 11):
    if abs(2*x - 1) <= 5:
        count += 1
        valid_integers.append(x)

# 정답이 6인지 확인
if count == 6 and valid_integers == [-2, -1, 0, 1, 2, 3]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')