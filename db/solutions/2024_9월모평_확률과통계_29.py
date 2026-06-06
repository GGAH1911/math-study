from fractions import Fraction
from math import comb

# 각 시행에서 뒤집을 확률
p_flip = Fraction(1, 4)
p_keep = Fraction(3, 4)

# 5번 시행 후 홀수 번 뒤집힐 확률
p_odd = Fraction(0)
for k in [1, 3, 5]:
    p_odd += comb(5, k) * (p_flip ** k) * (p_keep ** (5 - k))

print(f'p = {p_odd} = {float(p_odd)}')
print(f'128 * p = {128 * p_odd}')
print(f'Result: {int(128 * p_odd)}')

if int(128 * p_odd) == 62:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')