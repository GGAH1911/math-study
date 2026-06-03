from fractions import Fraction

n = 45
p = Fraction(1, 3)
q = 1 - p  # 2/3

V_X = n * p * q          # 45 * (1/3) * (2/3) = 10
V_2X = 4 * V_X           # 4 * 10 = 40

if V_2X == 40:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: V(2X) = {V_2X}')
