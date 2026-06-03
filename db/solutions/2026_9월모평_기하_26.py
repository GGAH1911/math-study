import math

# 좌표 설정
A = (0, 0, 0)
F = (10, 0, 1)
H = (0, 5, 1)

# 벡터
AF = (F[0] - A[0], F[1] - A[1], F[2] - A[2])
FH = (H[0] - F[0], H[1] - F[1], H[2] - F[2])

# 외적
cross = (
    AF[1] * FH[2] - AF[2] * FH[1],
    AF[2] * FH[0] - AF[0] * FH[2],
    AF[0] * FH[1] - AF[1] * FH[0]
)

# 거리 계산
cross_magnitude = math.sqrt(cross[0]**2 + cross[1]**2 + cross[2]**2)
FH_magnitude = math.sqrt(FH[0]**2 + FH[1]**2 + FH[2]**2)

distance = cross_magnitude / FH_magnitude

# 검증
expected = math.sqrt(21)
if abs(distance - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')