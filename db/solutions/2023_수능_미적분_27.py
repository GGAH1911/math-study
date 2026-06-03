from sympy import sqrt, Rational, simplify

# 원 조건 그대로
O = (Rational(0), Rational(0))
A1 = (Rational(1), Rational(0))
B1 = (Rational(0), Rational(1))

# OC1P1D1 직사각형, OC1:OD1=3:4, 대각선 OP1=1
# OC1=3k, OD1=4k -> 25k^2=1 -> k=1/5
k = Rational(1,5)
OC1, OD1 = 3*k, 4*k
P1 = (OC1, OD1)
# 호 위인지 확인: OP1^2 = 1
assert simplify(P1[0]**2 + P1[1]**2 - 1) == 0

# 이등변직각삼각형 P1 Q1 A1, 직각이 Q1
P1A1_sq = (P1[0]-A1[0])**2 + (P1[1]-A1[1])**2
area1 = P1A1_sq / 4  # = (빗변^2)/4

# Q1 좌표 결정 (두 후보 중 부채꼴 내부)
mid = ((P1[0]+A1[0])/2, (P1[1]+A1[1])/2)
dx, dy = A1[0]-P1[0], A1[1]-P1[1]
candA = (mid[0] - dy/2, mid[1] + dx/2)
candB = (mid[0] + dy/2, mid[1] - dx/2)
OQA = sqrt(candA[0]**2 + candA[1]**2)
OQB = sqrt(candB[0]**2 + candB[1]**2)
# 부채꼴(반지름 1) 내부의 것 선택
if OQA < 1 and (candA[0] >= 0 and candA[1] >= 0):
    Q1, OQ1 = candA, OQA
else:
    Q1, OQ1 = candB, OQB

# 이등변·직각 조건 재확인
P1Q = sqrt((P1[0]-Q1[0])**2 + (P1[1]-Q1[1])**2)
A1Q = sqrt((A1[0]-Q1[0])**2 + (A1[1]-Q1[1])**2)
assert simplify(P1Q - A1Q) == 0
# 내적이 0 (직각)
dot = (P1[0]-Q1[0])*(A1[0]-Q1[0]) + (P1[1]-Q1[1])*(A1[1]-Q1[1])
assert simplify(dot) == 0

# 닮음비
r2 = simplify(OQ1**2)  # 다음 부채꼴 반지름의 제곱(=넓이비)
limit = simplify(area1 / (1 - r2))

print('area1 =', area1, 'ratio^2 =', r2, 'limit =', limit)
print('VERIFY_PASS' if limit == Rational(1,4) else 'VERIFY_FAIL')
