from fractions import Fraction

# 히스토그램에서 읽은 데이터
# 각 구간별 일수
data = {
    (10, 20): 2,
    (20, 30): 7,
    (30, 40): 12,
    (40, 50): 6,
    (50, 60): 3,
    (60, 70): 0
}

# 전체 일수
total_days = sum(data.values())
assert total_days == 30, f"Total days should be 30, got {total_days}"

# 30개 이상인 일수 (30 ≤ 판매량)
days_30_or_more = data[(30, 40)] + data[(40, 50)] + data[(50, 60)] + data[(60, 70)]
days_30_or_more = 12 + 6 + 3 + 0
assert days_30_or_more == 21, f"Days >= 30 should be 21, got {days_30_or_more}"

# 비율 (백분율)
a = (days_30_or_more / total_days) * 100
assert a == 70, f"Percentage should be 70, got {a}"

print('VERIFY_PASS')