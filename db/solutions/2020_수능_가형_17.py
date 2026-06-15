import sympy as sp
from sympy import sqrt, symbols, solve, Rational

# 쌍곡선 위의 점 P와 조건 확인
y = Rational(24,5) * sqrt(3)
x_sq = 1 + y**2 / 24
x = sqrt(x_sq)

# 쌍곡선 조건 확인
hyperbola_check = x**2 - y**2/24 - 1
hyperbola_check = sp.simplify(hyperbola_check)

# PB, PC 거리
PB = sqrt((x + 5)**2 + y**2)
PC = sqrt((x - 5)**2 + y**2)
diff = sp.simplify(PB - PC)

# 삼각형 PBC 넓이 (BC=10, 높이=y)
area = Rational(1,2) * 10 * y
area = sp.simplify(area)

if hyperbola_check == 0 and sp.simplify(diff - 2) == 0 and sp.simplify(area - 24*sqrt(3)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')