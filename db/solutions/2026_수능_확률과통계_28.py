from itertools import product
from fractions import Fraction

count_total_odd = 0
count_favorable = 0

for rolls in product(range(1, 7), repeat=4):
    B = [0] * 7  # B[1]~B[6]
    
    for k in rolls:
        if k % 2 == 1:  # k 홀수: 상자 1,3,5에 +1
            B[1] += 1; B[3] += 1; B[5] += 1
        else:  # k 짝수: k의 약수가 적힌 상자에 +1
            for box in range(1, 7):
                if k % box == 0:
                    B[box] += 1
    
    total = sum(B[1:7])
    
    if total % 2 == 1:  # 총합 홀수
        count_total_odd += 1
        if B[3] == B[2] + 1:  # 상자3 = 상자2 + 1
            count_favorable += 1

prob = Fraction(count_favorable, count_total_odd)
expected = Fraction(3, 16)

if prob == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {prob}, expected {expected}')
