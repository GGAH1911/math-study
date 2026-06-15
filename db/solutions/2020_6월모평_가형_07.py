from itertools import combinations

# 조건을 만족하는 (a,b,c) 찾기
count = 0
valid_cases = []

for a in range(1, 12):
    for b in range(a+1, 12):
        for c in range(b+1, 12):
            if a + b + c == 12:
                count += 1
                valid_cases.append((a, b, c))

if count == 7:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: 실제 경우의 수 = {count}, 예상 = 7')