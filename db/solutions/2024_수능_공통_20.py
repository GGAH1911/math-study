import sympy as sp
from sympy import sqrt, symbols, solve, simplify

a = sqrt(sp.Rational(5, 2))
x = symbols('x', real=True)

# 원래 함수
f = -x**3 + a*x**2 + 2*x

# 점 A의 좌표
A_x = a
A_y = 2*a

# 점 B의 좌표
B_x = a**3 / (a**2 - 2)
B_y = 0

# 벡터 계산
AO = (-A_x, -A_y)
AB = (B_x - A_x, B_y - A_y)

# 원의 지름 조건 확인
dot_product = AO[0]*AB[0] + AO[1]*AB[1]
dot_product_simplified = simplify(dot_product)

# 거리 계산
OA = sqrt(A_x**2 + A_y**2)
AB_dist = sqrt((B_x - A_x)**2 + (B_y - A_y)**2)

OA_simplified = simplify(OA)
AB_simplified = simplify(AB_dist)

# 최종 답
result = simplify(OA_simplified * AB_simplified)

if abs(float(result) - 25.0) < 1e-10 and abs(float(dot_product_simplified)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')