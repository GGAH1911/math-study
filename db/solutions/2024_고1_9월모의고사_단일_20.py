from sympy import *

a_val = 12
A = Matrix([-8, a_val])
B = Matrix([7, 3])
C = Matrix([-6, 0])
O = Matrix([0, 0])

# P: 2:1 내분
P = (A + 2*B) / 3
assert P == Matrix([2, 6]), f'P wrong: {P}'

# 넓이 함수
def area(P1, P2, P3):
    v1 = P2 - P1; v2 = P3 - P1
    return Abs(v1[0]*v2[1] - v1[1]*v2[0]) / 2

area_AOB = area(A, O, B)

# Q: OA 위 t=1/4
t_val = Rational(1, 4)
Q = t_val * A

# Q가 직선 PC 위에 있는지 확인
# 직선 PC: y = ((a+6)/24)*(x+6)
lhs = Q[1]
rhs = (a_val + 6) * (Q[0] + 6) / 24
on_line = simplify(lhs - rhs) == 0

# 넓이 이등분 확인
area_APQ = area(A, P, Q)
bisect_ok = (area_APQ == area_AOB / 2)

if on_line and bisect_ok:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: on_line={on_line}, area_APQ={area_APQ}, area_AOB/2={area_AOB/2}')
