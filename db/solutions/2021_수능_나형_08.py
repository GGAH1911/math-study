from itertools import product

# 주사위 세 번, 곱이 4인 경우의 수
count = 0
for a, b, c in product(range(1, 7), repeat=3):
    if a * b * c == 4:
        count += 1

total = 6 ** 3
probability = count / total

# 기댓값: 1/36
expected = 1/36

if abs(probability - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')