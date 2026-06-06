from statistics import median, mode
import statistics

# 문제 조건
data_known = [9, 5, 6, 4, 8, 1]
a, b = 7, 8  # 또는 8, 7
c = 8

data = data_known + [a, b]
data_sorted = sorted(data)

# 평균 검증
mean_val = sum(data) / len(data)
assert mean_val == 6, f"평균 실패: {mean_val}"

# 중앙값 검증
median_val = (data_sorted[3] + data_sorted[4]) / 2
assert median_val == 6.5, f"중앙값 실패: {median_val}"

# 최빈값 검증
from collections import Counter
counter = Counter(data)
mode_val = max(counter, key=counter.get)
assert mode_val == c, f"최빈값 실패: {mode_val} != {c}"

# 모든 조건 만족
print('VERIFY_PASS')