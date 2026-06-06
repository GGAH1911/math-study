from itertools import combinations_with_replacement

# 13 이하의 자연수 중 조건을 만족하는 순서쌍 세기
count = 0
for a in range(1, 14):
    for b in range(a, 14):
        for c in range(b, 14):
            for d in range(c, 14):
                # 조건 검사
                if (a * d) % 2 == 1 and (b + c) % 2 == 0:  # a*d는 홀수, b+c는 짝수
                    count += 1

if count == 336:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: expected 336, got {count}')