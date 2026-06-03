import math
from decimal import Decimal, getcontext
getcontext().prec = 50

# x = 2 + 3√2
x = 2 + 3*math.sqrt(2)

# E, F, G 좌표
E = (x, 2)
F = (x-2, x)
G = (2*x-2, 0)

# 삼각형 EFG의 넓이 (좌표 공식)
area = abs((E[0]*(F[1]-G[1]) + F[0]*(G[1]-E[1]) + G[0]*(E[1]-F[1]))/2)

if abs(area - 7.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected: 7, Got: {area}')