from sympy import sqrt, simplify, Rational

CANDIDATE = 40

# 문제의 원래 조건들:
# - 정사각형 ABCD, 한 변 길이 8
# - P: AB 호의 삼등분점 중 B에 가까운 점 (접은 후)
# - Q: CD 호의 이등분점 (접은 후)
# - PG = 3 (P에서 평면 ABCD에 내린 수선의 발까지 거리)
# - QH = 2√3 (Q에서 평면 ABCD에 내린 수선의 발까지 거리)
# - G, H는 정사각형 ABCD 내부에 위치

# 좌표 설정
A = (0, 0, 0)
B = (8, 0, 0)
C = (8, 8, 0)  # 정사각형 한 변이 8
D = (0, 8, 0)

# AB 반원 호의 삼등분점 중 B에 가까운 점: 
# 반원의 반지름은 4, 평면상 좌표는 (6, -2√3, 0)
# AB를 축으로 각도 α만큼 접으면: P = (6, -2√3·cos(α), 2√3·sin(α))
# PG = 3 조건: 2√3·sin(α) = 3 → sin(α) = √3/2
# G가 정사각형 내부: cos(α) < 0 필요 → α = 2π/3
# P의 최종 좌표: (6, √3, 3)

# CD 반원 호의 이등분점:
# 반원의 반지름은 4, 평면상 좌표는 (4, 12, 0)  
# CD를 축으로 각도 β만큼 접으면: Q = (4, 8+4·cos(β), 4·sin(β))
# QH = 2√3 조건: 4·sin(β) = 2√3 → sin(β) = √3/2
# H가 정사각형 내부: 0 < 8+4·cos(β) < 8 필요 → cos(β) < 0 → β = 2π/3
# Q의 최종 좌표: (4, 6, 2√3)

P = (6, 3, sqrt(3))
Q = (4, 6, 2*sqrt(3))

# 조건 검증
PG = P[2]  # P에서 평면 ABCD까지의 높이
QH = Q[2]  # Q에서 평면 ABCD까지의 높이
G = (P[0], P[1], 0)  # P의 정사영
H = (Q[0], Q[1], 0)  # Q의 정사영

# G, H가 정사각형 내부인지 확인
assert 0 < G[0] < 8 and 0 < G[1] < 8, "G가 정사각형 내부에 없음"
assert 0 < H[0] < 8 and 0 < H[1] < 8, "H가 정사각형 내부에 없음"

# 평면 PCQ의 법선 벡터 계산
CP = (P[0] - C[0], P[1] - C[1], P[2] - C[2])
CQ = (Q[0] - C[0], Q[1] - C[1], Q[2] - C[2])

# 외적 계산
normal = (
    CP[1] * CQ[2] - CP[2] * CQ[1],
    CP[2] * CQ[0] - CP[0] * CQ[2],
    CP[0] * CQ[1] - CP[1] * CQ[0]
)

# 정규화하여 간단히
normal = tuple(simplify(n) for n in normal)

# 법선의 크기 제곱
mag_squared = sum(n**2 for n in normal)
mag_squared = simplify(mag_squared)

# 두 평면의 각도 θ 계산
# 평면 ABCD의 법선: (0, 0, 1)
# cos(θ) = |normal·(0,0,1)| / |normal| = |normal[2]| / √(mag_squared)
cos_squared_theta = (normal[2]**2) / mag_squared
cos_squared_theta = simplify(cos_squared_theta)

# 최종 계산: 70·cos²(θ)
result = 70 * cos_squared_theta
result = simplify(result)

# CANDIDATE 검증
if result == CANDIDATE:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL")