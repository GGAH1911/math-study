# X = 앞뒤 숫자가 다른 카드 개수
# (a1, a2, a3)는 {1,2,3,4,5}에서 순서 고려 3개 선택

count = {0: 0, 1: 0, 2: 0, 3: 0}

for a1 in range(1, 6):
    for a2 in range(1, 6):
        if a2 == a1:
            continue
        for a3 in range(1, 6):
            if a3 == a1 or a3 == a2:
                continue
            # 뒷면은 1, 2, 3
            diff = 0
            if a1 != 1: diff += 1
            if a2 != 2: diff += 1
            if a3 != 3: diff += 1
            count[diff] += 1

prob = {k: v/60 for k, v in count.items()}
EX = sum(k * prob[k] for k in range(4))

a = prob[1]
b = prob[2]
c = EX
result = 10*a + 20*b + 5*c

if abs(result - 20) < 0.001:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}')