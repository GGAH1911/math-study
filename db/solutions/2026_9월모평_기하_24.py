# 두 직선의 방향벡터 확인
# 직선1: (x-1)/2 = y-4 → 방향벡터 (2, 1)
# 직선2: (x+2)/8 = (y+5)/a → 방향벡터 (8, a)

a = 4

# 방향벡터
v1 = (2, 1)
v2 = (8, a)

# 평행 조건: 외적이 0
cross_product = v1[0] * v2[1] - v1[1] * v2[0]
if cross_product == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')