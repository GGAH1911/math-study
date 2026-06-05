import math
from sympy import sqrt, symbols, solve

# 좌표 설정
A = (1, 2)
B = (0, 0)
C = (4, 0)
D = (3, 2)

# 조건 검증
# 1. AD || BC
AD_vec = (D[0]-A[0], D[1]-A[1])  # (2, 0)
BC_vec = (C[0]-B[0], C[1]-B[1])  # (4, 0)
# 평행: 외적이 0
cross = AD_vec[0]*BC_vec[1] - AD_vec[1]*BC_vec[0]
assert cross == 0, f"AD와 BC가 평행하지 않음: {cross}"

# 2. |AD| = 2
AD_len = math.sqrt((D[0]-A[0])**2 + (D[1]-A[1])**2)
assert abs(AD_len - 2) < 1e-9, f"|AD| = {AD_len}, expected 2"

# 3. |BC| = 4
BC_len = math.sqrt((C[0]-B[0])**2 + (C[1]-B[1])**2)
assert abs(BC_len - 4) < 1e-9, f"|BC| = {BC_len}, expected 4"

# 4. ∠CBA = ∠DCB
import math
# ∠CBA: B에서 BA와 BC의 각
BA_vec = (A[0]-B[0], A[1]-B[1])  # (1, 2)
BC_vec = (C[0]-B[0], C[1]-B[1])  # (4, 0)
tan_CBA = BA_vec[1] / BA_vec[0]  # 2/1 = 2

# ∠DCB: C에서 CD와 CB의 각
CD_vec = (D[0]-C[0], D[1]-C[1])  # (-1, 2)
CB_vec = (B[0]-C[0], B[1]-C[1])  # (-4, 0)
# CB 방향을 x축의 음의 방향으로 정규화하면, CD와 이루는 각의 탄젠트는
tan_DCB = abs(CD_vec[1]) / abs(CD_vec[0])  # 2/1 = 2
assert abs(tan_CBA - tan_DCB) < 1e-9, f"tan(∠CBA) = {tan_CBA}, tan(∠DCB) = {tan_DCB}"

# 5. |AB + AC| = 2√5
AB_vec = (B[0]-A[0], B[1]-A[1])  # (-1, -2)
AC_vec = (C[0]-A[0], C[1]-A[1])  # (3, -2)
sum_vec = (AB_vec[0]+AC_vec[0], AB_vec[1]+AC_vec[1])  # (2, -4)
sum_len = math.sqrt(sum_vec[0]**2 + sum_vec[1]**2)  # √20 = 2√5
expected = 2 * math.sqrt(5)
assert abs(sum_len - expected) < 1e-9, f"|AB+AC| = {sum_len}, expected {expected}"

# BD 계산
BD_len = math.sqrt((D[0]-B[0])**2 + (D[1]-B[1])**2)
expected_BD = math.sqrt(13)
assert abs(BD_len - expected_BD) < 1e-9, f"|BD| = {BD_len}, expected {expected_BD}"

print('VERIFY_PASS')