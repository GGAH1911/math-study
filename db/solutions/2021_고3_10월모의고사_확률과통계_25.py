from math import comb

# 중복조합: a' + b' + c + d = 6 (모두 음이 아닌 정수)
# 4개 변수, 합이 6
result = comb(6 + 4 - 1, 4 - 1)
print(f'음이 아닌 정수해의 개수: {result}')

# 검증: 직접 세기로 확인
count = 0
for a_prime in range(7):
    for b_prime in range(7 - a_prime):
        for c in range(7 - a_prime - b_prime):
            d = 6 - a_prime - b_prime - c
            if d >= 0:
                a = a_prime + 2
                b = b_prime + 2
                # 원래 조건: a + b + c + d = 10, a >= 2, b >= 2, c >= 0, d >= 0
                if a + b + c + d == 10 and a >= 2 and b >= 2 and c >= 0 and d >= 0:
                    count += 1

if result == count == 84:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')