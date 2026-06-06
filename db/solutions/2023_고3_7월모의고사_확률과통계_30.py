from itertools import product

CANDIDATE = 150

X = [1, 2, 3, 4, 5, 6, 7]
count = 0

# 모든 함수 f: X → X 생성
for f_tuple in product(X, repeat=7):
    f = list(f_tuple)  # f[0] = f(1), f[1] = f(2), ..., f[6] = f(7)
    
    # 조건 (가): f(7) - f(1) = 3
    if f[6] - f[0] != 3:
        continue
    
    # 조건 (나): f(n) ≤ f(n+2) for n = 1, 2, 3, 4, 5
    # f(1) ≤ f(3), f(2) ≤ f(4), f(3) ≤ f(5), f(4) ≤ f(6), f(5) ≤ f(7)
    if not (f[0] <= f[2] and f[1] <= f[3] and f[2] <= f[4] and f[3] <= f[5] and f[4] <= f[6]):
        continue
    
    # 조건 (다)-①: (1/3)|f(2) - f(1)|이 자연수
    # |f(2) - f(1)| ∈ {3, 6} (0은 불가, 자연수는 양수)
    diff = abs(f[1] - f[0])
    if diff == 0 or diff % 3 != 0:
        continue
    
    # 조건 (다)-②: (1/3)(f(1) + f(3) + f(5) + f(7))이 자연수
    # f(1) + f(3) + f(5) + f(7) ≡ 0 (mod 3)
    odd_sum = f[0] + f[2] + f[4] + f[6]
    if odd_sum % 3 != 0:
        continue
    
    count += 1

if count == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")