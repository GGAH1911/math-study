from sympy import Rational, Rational

a = Rational(2, 3)

# 원래 조건
AB = 3*a**2 + 10*a + 7
AD = a
AE = a

# P: AB를 1:a 내분
AP = AB * 1 / (1 + a)

# 사다리꼴 AEFP 넓이 (평행변 AP, EF=AB, 높이 AE)
trap_area = Rational(1,2) * (AP + AB) * AE

# V1: 사각기둥 AEFP-DHGQ
V1 = trap_area * AD

# 삼각형 PFB 넓이 (직각변 PB=(AB-AP), BF=AE)
tri_area = Rational(1,2) * (AB - AP) * AE

# V2: 삼각기둥 PFB-QGC
V2 = tri_area * AD

diff = V1 - V2

if diff == 4 and AP == 9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: V1-V2={diff}, AP={AP}')
