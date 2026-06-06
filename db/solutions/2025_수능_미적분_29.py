import sympy as sp
from fractions import Fraction

# 등비수열 a_n = 5 * (-1/2)^(n-1)
def a(n):
    return 5 * (Fraction(-1, 2))**(n-1)

# m에 대한 극한값 계산
def limit_value(m):
    # 극한값 = 2*(-1)^(m+1) / 2^m
    return 2 * ((-1)**(m+1)) / (2**m)

threshold = Fraction(1, 700)
valid_m = []

for m in range(1, 15):
    limit_val = limit_value(m)
    if limit_val > threshold:
        valid_m.append(m)
        
# 검증
if set(valid_m) == {1, 3, 5, 7, 9}:
    total = sum(valid_m)
    if total == 25:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')