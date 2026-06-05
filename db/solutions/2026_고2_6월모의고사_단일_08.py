import math
import numpy as np

# 답: 3π/2
ans = 3 * math.pi / 2

# 범위
alpha = math.pi / 4
beta = 7 * math.pi / 4

# α, β가 부등식 2cos(x) - √2 = 0을 만족하는지 확인
cos_alpha = math.cos(alpha)
cos_beta = math.cos(beta)

# cos(π/4) = √2/2, cos(7π/4) = √2/2
expected_cos = math.sqrt(2) / 2

assert abs(cos_alpha - expected_cos) < 1e-10, f"cos(α) = {cos_alpha}, expected {expected_cos}"
assert abs(cos_beta - expected_cos) < 1e-10, f"cos(β) = {cos_beta}, expected {expected_cos}"

# 범위 내 샘플점 확인: x ∈ [π/4, 7π/4]에서 2cos(x) - √2 ≤ 0
test_points = [math.pi / 4, math.pi / 2, math.pi, 3 * math.pi / 2, 7 * math.pi / 4]
for x in test_points:
    val = 2 * math.cos(x) - math.sqrt(2)
    assert val <= 1e-10, f"x={x}: 2cos(x) - √2 = {val} (should be ≤ 0)"

# 범위 밖 샘플점 확인: 일부 x가 부등식을 만족하지 않아야 함
outside_point = math.pi / 8  # π/4보다 작은 구간
val_outside = 2 * math.cos(outside_point) - math.sqrt(2)
assert val_outside > 1e-10, f"Outside point should not satisfy: {val_outside}"

# β - α 확인
diff = beta - alpha
expected_diff = 3 * math.pi / 2
assert abs(diff - expected_diff) < 1e-10, f"β - α = {diff}, expected {expected_diff}"

print('VERIFY_PASS')