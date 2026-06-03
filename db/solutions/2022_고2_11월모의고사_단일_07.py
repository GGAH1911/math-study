# 그래프에서 읽은 극한값들
left_f, right_f = 2, -1
left_g, right_g = -1, 1
k = 3/2

# 극한 존재 조건: 좌극한 = 우극한
left_total = left_f + k * left_g
right_total = right_f + k * right_g

if abs(left_total - right_total) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')