from sympy import symbols, solve, Abs

# 각 d 값에 대해 검증
test_cases = [(128, 1), (32, 3), (8, 7), (2, 15)]
valid_d = []

for d, m in test_cases:
    # a_1 계산
    a1 = -((3*m - 2)*d) // 2
    
    # 조건 (나) 검증: a_{2m} = -a_m
    a_m = a1 + (m - 1)*d
    a_2m = a1 + (2*m - 1)*d
    
    if a_2m != -a_m:
        continue
    
    # 합 계산
    total_sum = sum(abs(a1 + (k - 1)*d) for k in range(m, 2*m + 1))
    
    if total_sum != 128:
        continue
    
    # 조건 (가) 검증: 모든 자연수 n에 대해 a_n ≠ 0
    is_valid = True
    for n in range(1, 100):  # 충분한 범위
        if a1 + (n - 1)*d == 0:
            is_valid = False
            break
    
    if is_valid:
        valid_d.append(d)

if sum(valid_d) == 170:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')