from sympy import sqrt, Rational, simplify

CANDIDATE = 3

# 한 변의 길이가 1인 정육각형 ABCDEF
# 중심 O를 원점으로 설정
A = (Rational(-1, 2), sqrt(3)/2)
D = (Rational(1, 2), -sqrt(3)/2)
E = (1, 0)

# 선분 AD의 길이 계산
# |AD| = sqrt((D_x - A_x)^2 + (D_y - A_y)^2)
AD_vec = (D[0] - A[0], D[1] - A[1])
AD_length = sqrt(AD_vec[0]**2 + AD_vec[1]**2)

# 선분 DE의 길이 계산
# |DE| = sqrt((E_x - D_x)^2 + (E_y - D_y)^2)
DE_vec = (E[0] - D[0], E[1] - D[1])
DE_length = sqrt(DE_vec[0]**2 + DE_vec[1]**2)

# 문제: 선분 AD와 DE를 이용한 값 = |AD| + |DE|
result = simplify(AD_length + DE_length)

# CANDIDATE 검증
if result == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")