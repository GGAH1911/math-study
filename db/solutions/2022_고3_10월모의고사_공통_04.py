# 그래프에서 직접 읽은 극한값 검증
lim_at_minus1_plus = 4
lim_at_2_minus = -2

result = lim_at_minus1_plus + lim_at_2_minus
print('VERIFY_PASS' if result == 2 else 'VERIFY_FAIL')