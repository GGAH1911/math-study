import math
from scipy.optimize import fsolve

def verify_condition(n):
    log2_n = math.log2(n)
    # 이차부등식: 3x^2 - 2(log_2 n)x + log_2 n > 0 이 모든 x에서 성립하는지 확인
    # 판별식이 음수여야 함
    discriminant = 4 * log2_n**2 - 12 * log2_n
    return discriminant < 0

count = 0
for n in range(1, 20):
    if verify_condition(n):
        count += 1
        print(f'n={n}: log2(n)={math.log2(n):.4f}, D={4*math.log2(n)**2 - 12*math.log2(n):.4f} < 0')

if count == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')