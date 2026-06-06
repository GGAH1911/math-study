import sympy as sp
from sympy import symbols, simplify, expand

# 기호 정의
a_n = symbols('a_n', positive=True, real=True)

# 점들의 좌표
P_n = (a_n, 0)
Q_n = (a_n, a_n**3)
P_n1 = (a_n + a_n**5, 0)

# 삼각형 OP_{n+1}Q_n의 넓이 계산 (밑변 × 높이 / 2)
base = a_n + a_n**5
height = a_n**3
area = base * height / 2

# 정리
area_simplified = simplify(expand(area))
print(f'Area = {area_simplified}')

# 원래 식과 비교: (1/2)*a_n^4*(1 + a_n^4)
original = sp.Rational(1, 2) * a_n**4 * (1 + a_n**4)
original_expanded = expand(original)
print(f'Expected = {original_expanded}')

# 검증
if simplify(area_simplified - original_expanded) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')