# 주어진 조건에서 샌드위치 정리를 적용하여 극한값 검증
lim_left = 1/3
lim_right = 1/3
expected = 1/3

# 큰 n값에서 좌극한과 우극한이 1/3으로 수렴하는지 확인
for n in [50, 100, 200]:
    left = (3**n - 2**n) / (3**(n+1) + 2**n)
    right = (3**n + 2**n) / (3**(n+1) + 2**n)
    assert abs(left - 1/3) < 1e-6
    assert abs(right - 1/3) < 1e-6

print('VERIFY_PASS')