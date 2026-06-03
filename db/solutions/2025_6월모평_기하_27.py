from sympy import *

c = symbols('c', positive=True)
a_sym = 3*c
b_sym = 2*sqrt(2)*c

# 넓이 조건
c_val = solve(Eq(4*a_sym*b_sym, 32*sqrt(2)), c)[0]
a_num = 3*c_val
b_num = 2*sqrt(2)*c_val

# 초점
F = (a_num + c_val, b_num)
Fp = (a_num - c_val, b_num)

# FF' 거리
FF = simplify(sqrt((F[0]-Fp[0])**2 + (F[1]-Fp[1])**2))

# 포물선 검증 함수 (초점 F, 준선 x=0)
def parabola_residual(pt, focus):
    x, y = pt
    fx, fy = focus
    return simplify(sqrt((x-fx)**2 + (y-fy)**2) - x)

chk_Fp = parabola_residual(Fp, F)          # F' on parabola
chk_Q  = parabola_residual((a_num, S.Zero), F)  # Q on parabola
chk_S  = parabola_residual((a_num, 2*b_num), F) # S on parabola

expected = Rational(4,3)*sqrt(3)

if (simplify(FF - expected) == 0
        and chk_Fp == 0
        and chk_Q  == 0
        and chk_S  == 0):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'FF={FF}, expected={expected}')
    print(f'chk_Fp={chk_Fp}, chk_Q={chk_Q}, chk_S={chk_S}')
