CANDIDATE = 12

# 주어진 조건
n = 16
sample1_mean = 75
sample2_mean = 77
z_95 = 1.96
z_99 = 2.58
diff_target = 3.86

sigma = CANDIDATE

# 신뢰구간 계산
margin1 = z_95 * (sigma / (n ** 0.5))
margin2 = z_99 * (sigma / (n ** 0.5))

b = sample1_mean + margin1
d = sample2_mean + margin2

# 조건 확인
diff = d - b
print(f'b = {b}')
print(f'd = {d}')
print(f'd - b = {diff}')

if abs(diff - diff_target) < 0.0001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')