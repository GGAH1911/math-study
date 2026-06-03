import sympy as sp
p = sp.Rational(3, 1)
# 포물선 y^2 = 4px에서 초점 F = (p, 0), 준선 x = -p
# 포물선 위의 점 (x, y)에서 초점까지의 거리 = x + p
FP1 = 1*p + p  # x = p
FP2 = 2*p + p  # x = 2p
FP3 = 3*p + p  # x = 3p
total = FP1 + FP2 + FP3
if total == 27:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {total}')