from sympy import *

A = Matrix([Rational(7,2), 3*sqrt(7)/2])
B = Matrix([0, 0])
C = Matrix([6, 0])
P = Matrix([3, 0])
Q = Matrix([5, 0])

# 원래 조건 검증
AB = (A-B).norm()
AQ_len = (A-Q).norm()
PQ_len = (Q-P).norm()
BQ_len = (Q-B).norm()
QC_len = (C-Q).norm()

assert simplify(AB - 2*sqrt(7)) == 0, 'AB 실패'
assert simplify(AQ_len - 3*sqrt(2)) == 0, 'AQ 실패'
assert simplify(P - (B+C)/2) == Matrix([0,0]), 'P 중점 실패'
assert simplify(BQ_len/QC_len - 5) == 0, 'Q 5:1 내분 실패'

# 정현 비율 검증
sin_ratio = simplify(PQ_len / AQ_len)
assert simplify(sin_ratio - sqrt(2)/3) == 0, '정현 비율 실패'

# 외접원 넓이 계산
BC = (C-B).norm()
CA = (C-A).norm()
v1 = B - A; v2 = C - A
area = Abs(v1[0]*v2[1] - v1[1]*v2[0]) / 2
R = AB * BC * CA / (4 * area)
circle_area = simplify(pi * R**2)

expected = Rational(88,9)*pi
if simplify(circle_area - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', circle_area)
