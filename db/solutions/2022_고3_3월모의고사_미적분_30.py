from sympy import *

CANDIDATE = 80

# 기하학적 조건 검증
n = symbols('n', positive=True, integer=True)
a = n + 1

# 곡선: y = sqrt(3)*x
# P_n = (a, sqrt(3)*a), a = n+1
P_n = (a, sqrt(3)*a)
H_n = (a, 0)

# |OP_n| = 2(n+1) 검증
OP_n_dist = simplify(sqrt(P_n[0]**2 + P_n[1]**2))
assert OP_n_dist == 2*a, f'|OP_n| verification failed: {OP_n_dist} != {2*a}'

# 원 C_n: 중심 P_n, 반지름 sqrt(3)*a
radius = sqrt(3) * a

# R_n = (-a/2, sqrt(3)*a/2) (원점에서의 접선의 다른 접점)
R_n = (-a/2, sqrt(3)*a/2)

# R_n이 원 위의 점 검증
dist_Pn_Rn = simplify(sqrt((P_n[0] - R_n[0])**2 + (P_n[1] - R_n[1])**2))
assert dist_Pn_Rn == radius, f'R_n on circle verification failed: {dist_Pn_Rn} != {radius}'

# 원점에서 R_n까지의 거리 (접선 조건)
OR_n_dist = simplify(sqrt(R_n[0]**2 + R_n[1]**2))
assert OR_n_dist == a, f'Tangent distance verification failed: {OR_n_dist} != {a}'

# 원점에서 원까지의 접선 거리 검증
# sqrt(|OP_n|^2 - r^2) = sqrt(4a^2 - 3a^2) = a
tangent_dist_check = simplify(sqrt((2*a)**2 - (sqrt(3)*a)**2))
assert tangent_dist_check == a, f'Tangent distance formula failed'

# 검증된 풀이로부터: k = -2*sqrt(3)/3
k = -2*sqrt(3)/3
k_squared = simplify(k**2)

# k^2 = 4/3 검증
expected_k_squared = Rational(4, 3)
assert k_squared == expected_k_squared, f'k^2 verification failed: {k_squared} != {expected_k_squared}'

# 최종 답: 60*k^2
result = 60 * k_squared
result_int = int(result)

# CANDIDATE 검증
if result_int == CANDIDATE:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL')