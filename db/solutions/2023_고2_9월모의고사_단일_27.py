CANDIDATE = 74

import math

def roots_sum_cos_equation(c, interval_min=0, interval_max=4):
    """
    [interval_min, interval_max]에서 cos(π*x) = c의 모든 실근의 합을 구한다.
    """
    if c < -1 or c > 1:
        return 0.0
    
    roots = []
    eps = 1e-10
    
    # c = 1인 경우: cos(π*x) = 1 → x = 0, 2, 4, ...
    if abs(c - 1) < eps:
        for k in range(10):
            x = 2 * k
            if interval_min <= x <= interval_max:
                roots.append(x)
        return float(sum(roots))
    
    # c = -1인 경우: cos(π*x) = -1 → x = 1, 3, 5, ...
    if abs(c + 1) < eps:
        for k in range(10):
            x = 1 + 2 * k
            if interval_min <= x <= interval_max:
                roots.append(x)
        return float(sum(roots))
    
    # -1 < c < 1인 경우
    # x ∈ [0, 4]에서 π*x ∈ [0, 4π]
    # cos(θ) = c의 주기해: θ = ±arccos(c) + 2πk
    acos_c = math.acos(c)  # [0, π]
    
    # [0, 4π] 범위에서의 4개 해
    candidates_theta = [
        acos_c,
        2 * math.pi - acos_c,
        2 * math.pi + acos_c,
        4 * math.pi - acos_c
    ]
    
    for theta in candidates_theta:
        x = theta / math.pi
        if interval_min <= x <= interval_max:
            if abs(math.cos(theta) - c) < eps:
                roots.append(x)
    
    return float(sum(roots))

# |f(x)| = 3 → f(x) = 3 또는 f(x) = -3
# f(x) = (n/2)*cos(πx) + 1

total_g = 0.0

for n in range(4, 11):
    g_n = 0.0
    
    # 경우 1: (n/2)*cos(πx) + 1 = 3
    #         → (n/2)*cos(πx) = 2
    #         → cos(πx) = 4/n
    c1 = 4.0 / n
    g_n += roots_sum_cos_equation(c1)
    
    # 경우 2: (n/2)*cos(πx) + 1 = -3
    #         → (n/2)*cos(πx) = -4
    #         → cos(πx) = -8/n
    c2 = -8.0 / n
    g_n += roots_sum_cos_equation(c2)
    
    total_g += g_n

# CANDIDATE와 실제 계산값 비교
if abs(total_g - CANDIDATE) < 0.01:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")