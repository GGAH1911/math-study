from math import factorial, perm, comb

CANDIDATE = 200

# 계산
p_5_2 = perm(5, 2)  # 5P2
c_5_2 = comb(5, 2)  # 5C2
result = p_5_2 * c_5_2

if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: expected {result}, got {CANDIDATE}')