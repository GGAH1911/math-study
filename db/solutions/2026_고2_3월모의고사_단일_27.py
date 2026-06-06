# 모든 가능한 배치를 직접 계산
chairs = [11, 12, 21, 22, 31, 32, 41, 42]
odd_chairs = [c for c in chairs if c % 10 == 1]  # 홀수: 11, 21, 31, 41
le32_chairs = [c for c in chairs if c <= 32]  # 32이하: 11, 12, 21, 22, 31, 32
ge31_chairs = [c for c in chairs if c >= 31]  # 31이상: 31, 32, 41, 42

count = 0
for a in odd_chairs:
    for b in le32_chairs:
        if b == a:
            continue
        for c in ge31_chairs:
            if c == a or c == b:
                continue
            for d in ge31_chairs:
                if d == a or d == b or d == c:
                    continue
                count += 1

if count == 150:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected 150, got {count}')