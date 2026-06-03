# 줄기와 잎 그림으로부터 데이터 복원
data = [1, 8, 9, 12, 15, 15, 16, 17, 18, 19, 21, 23, 24, 24, 27, 32, 35, 37, 38, 42]
assert len(data) == 20, f'전체 인원은 20명이어야 함'

# 각 계급별 개수
count_0_10 = sum(1 for x in data if 0 <= x < 10)
count_10_20 = sum(1 for x in data if 10 <= x < 20)
count_20_30 = sum(1 for x in data if 20 <= x < 30)
count_30_40 = sum(1 for x in data if 30 <= x < 40)
count_40_50 = sum(1 for x in data if 40 <= x < 50)

assert count_0_10 == 3 and count_10_20 == 7 and count_20_30 == 5 and count_30_40 == 4 and count_40_50 == 1

# 상대도수 계산
p = count_10_20 / 20  # 0.35
q = count_20_30 / 20  # 0.25

# 검증: 상대도수 합 = 1
total_relative_freq = 0.15 + p + q + 0.2 + 0.05
assert abs(total_relative_freq - 1.0) < 1e-10, f'상대도수 합: {total_relative_freq}'

# 답 확인
result = p - q
assert abs(result - 0.1) < 1e-10, f'p - q = {result}'
print('VERIFY_PASS')