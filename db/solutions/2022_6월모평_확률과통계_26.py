from itertools import product

# 흰 카드 4장, 파란 카드 2장, 노란 카드 1장을 학생 3명에게 나누어주는 모든 경우
count = 0
for whites in product(range(5), repeat=3):
    if sum(whites) != 4:
        continue
    for blues in product(range(3), repeat=3):
        if sum(blues) != 2:
            continue
        for yellows in product(range(2), repeat=3):
            if sum(yellows) != 1:
                continue
            # 어떤 학생이 3가지 색을 모두 받는지 확인
            for i in range(3):
                if whites[i] >= 1 and blues[i] >= 1 and yellows[i] >= 1:
                    count += 1
                    break

if count == 90:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}, expected 90')