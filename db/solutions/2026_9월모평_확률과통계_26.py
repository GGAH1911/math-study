import numpy as np

# 주어진 값
sigma = 2 * np.sqrt(2)
n = 128
z_critical = 1.96

# 신뢰구간의 오차한계 c 계산
c = z_critical * sigma / np.sqrt(n)

print(f"c = {c}")
print(f"c (반올림) = {round(c, 2)}")

# 검증: c = 0.49
if abs(c - 0.49) < 0.001:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")