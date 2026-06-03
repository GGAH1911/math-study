count = 0
for a in range(1, 11):
    for b in range(1, 11):
        for c in range(1, 11):
            for d in range(1, 11):
                if a * b * c * d == 108:
                    nums = [a, b, c, d]
                    # 조건(나): 서로 같은 수가 있다 (= 4개가 모두 다르지 않다)
                    has_equal = len(set(nums)) < 4
                    if has_equal:
                        count += 1
if count == 40:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: count={count}')