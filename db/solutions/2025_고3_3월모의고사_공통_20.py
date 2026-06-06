from sympy import sqrt, pi, simplify, Rational, numer, denom

# 계산된 좌표 검증
A = (Rational(11, 2), sqrt(7)/2)
B = (0, 0)
C = (8, 0)
D = (6, 0)

# 조건 1: D는 BC를 3:1로 내분
assert D[0] == Rational(3, 4) * C[0], 'D 위치 오류'

# 조건 2: AD = sqrt(2)
AD = sqrt((A[0] - D[0])**2 + (A[1] - D[1])**2)
assert simplify(AD - sqrt(2)) == 0, 'AD 검증 실패'

# 조건 3: AB : AC = 2 : 1
AB = sqrt(A[0]**2 + A[1]**2)
AC = sqrt((A[0] - C[0])**2 + (A[1] - C[1])**2)
assert simplify(AB - 2*AC) == 0, 'AB:AC 검증 실패'

# 조건 4: cos(angle ADB) = sqrt(2)/4
DA = (A[0] - D[0], A[1] - D[1])
DB = (B[0] - D[0], B[1] - D[1])
cos_angle = (DA[0]*DB[0] + DA[1]*DB[1]) / (sqrt(DA[0]**2 + DA[1]**2) * sqrt(DB[0]**2 + DB[1]**2))
assert simplify(cos_angle - sqrt(2)/4) == 0, 'cos(θ) 검증 실패'

# 외접원 반지름
sin_theta = simplify(sqrt(1 - Rational(2, 16)))
R = simplify(AB / (2 * sin_theta))

# 외접원 넓이
area = pi * R**2
area_coeff = simplify(area / pi)
q = numer(area_coeff)
p = denom(area_coeff)

assert p + q == 71, f'최종 답 검증 실패: {p + q}'
print('VERIFY_PASS')