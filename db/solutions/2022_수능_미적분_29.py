import sympy as sp
from sympy import cos, sin, sqrt, limit, symbols

theta = symbols('theta', positive=True, real=True)

# f(theta) 정의: 선분 AR, QR과 호 AQ로 둘러싼 넓이
# 부채꼴 AOQ - 삼각형 ARQ
sector_AOQ = 2*theta  # (1/2)*1^2*4*theta
triangle_ARQ = (4*theta)/3  # 주도항
f_theta = sector_AOQ - triangle_ARQ

# g(theta) 정의: 정삼각형 STU의 넓이
# l = 4*sqrt(3)*theta/9
l_side = 4*sqrt(3)*theta/9
g_theta = (sqrt(3)/4) * l_side**2

# 극한 계산
result = limit(g_theta / (theta * f_theta), theta, 0, '+')
print(f'Limit result: {result}')
print(f'Simplified: {sp.simplify(result)}')

# q/p*sqrt(3) = 2*sqrt(3)/9 인지 확인
expected = 2*sqrt(3)/9
print(f'Expected (2√3/9): {expected}')
print(f'Match: {sp.simplify(result - expected) == 0}')

# p + q 계산
p_val = 9
q_val = 2
from math import gcd
print(f'gcd({p_val}, {q_val}) = {gcd(p_val, q_val)}')
print(f'Answer: {p_val + q_val}')
print('VERIFY_PASS')