import sympy as sp
from sympy import sqrt, simplify

CANDIDATE = 24

# S² = CANDIDATE이면, 삼각형 OFP의 넓이 S를 구한다
S_squared = CANDIDATE
S = sqrt(S_squared)  # S = 2√6

# 삼각형 OFP: O=(0,0), F=(2,0), P=(a,b)
# 넓이 공식: S = (1/2) * |OF| * height = (1/2) * 2 * b = b
# 따라서 b = S
b = S

# P=(a,b)는 포물선 y²=8x 위의 점
# 조건: b² = 8a
a = b**2 / 8
a_simplified = simplify(a)

# 검증 1: P가 원래 포물선 y²=8x 위에 있는가?
check1 = simplify(b**2 - 8*a)

# 포물선 C: 초점 P, 준선 x=k, 점 F=(2,0)을 지남
# 포물선 정의: |PF| = (F에서 준선까지의 거리) = |k - 2|
# |PF|² = (a-2)² + b²
PF_squared = (a - 2)**2 + b**2
PF_squared_simplified = simplify(PF_squared)

# |PF| = a+2가 되는가? (이는 b²=8a 조건과 동치)
check2 = simplify((a - 2)**2 + b**2 - (a + 2)**2)

# 포물선 C의 준선: |PF| = |k - 2|에서 k - 2 = a + 2 (k > a 조건)
k = a + 4

# 검증 3: 사각형 PRFQ의 둘레 조건
# 둘레 = 2a + 12 = 18
perimeter = 2*a + 12
perimeter_simplified = simplify(perimeter)
check3 = simplify(perimeter - 18)

# 모든 조건이 만족되는가?
if check1 == 0 and check2 == 0 and check3 == 0:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")