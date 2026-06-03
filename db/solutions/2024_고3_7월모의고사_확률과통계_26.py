from itertools import product

count = 0
total = 0
for n1, n2, n3 in product(range(1, 7), repeat=3):
    boxes = [False] * 8  # index 1~7 사용
    # 1번 시행
    if not boxes[n1]:
        boxes[n1] = True
    else:
        boxes[7] = True
    # 2번 시행
    if not boxes[n2]:
        boxes[n2] = True
    else:
        boxes[7] = True
    # 3번 시행
    if not boxes[n3]:
        boxes[n3] = True
    else:
        boxes[7] = True
    if boxes[7]:
        count += 1
    total += 1

from fractions import Fraction
prob = Fraction(count, total)
expected = Fraction(4, 9)
if prob == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {prob}, expected {expected}')
