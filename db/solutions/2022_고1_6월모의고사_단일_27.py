import numpy as np
from sympy import I, simplify

# 모든 n ≡ 3 (mod 4)인 경우를 확인
valid_n = [n for n in range(1, 101) if n % 4 == 3]
count = 0

for n in valid_n:
    # (1-i)^(2n) 계산
    z = (1 - I)**(2*n)
    # 2^n * i 계산
    target = 2**n * I
    # 검증
    if simplify(z - target) == 0:
        count += 1

if count == 25:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: found {count} instead of 25')