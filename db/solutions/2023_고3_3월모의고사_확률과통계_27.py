from math import comb

# 원래 조건: a + b + c + 3d = 10 (a,b,c,d는 자연수)
total_count = 0

# d' = d-1, 나머지도 -1 치환했을 때 a' + b' + c' + 3d' = 4
# d'의 가능한 값들
for d_prime in range(0, 5):
    remainder = 4 - 3 * d_prime
    if remainder < 0:
        break
    # a' + b' + c' = remainder의 음이 아닌 정수해 개수
    count = comb(remainder + 2, 2)
    total_count += count
    
print(f"음이 아닌 정수해 총 개수: {total_count}")

# 검증: 실제로 a+b+c+3d=10을 만족하는 자연수 순서쌍 세기
verify_count = 0
for a in range(1, 10):
    for b in range(1, 10):
        for c in range(1, 10):
            for d in range(1, 4):
                if a + b + c + 3*d == 10:
                    verify_count += 1

print(f"직접 계산 검증: {verify_count}")
if verify_count == 18:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")