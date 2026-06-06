import math
from math import pow

# 원래 식 계산
result = pow(3, 1/3) * pow(9, 1/4)
print(f'√[3](3) × √[4](9) = {result:.6f}')

# 답 검증: 3이 맞는지 확인
if 2.4 < result < 2.6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')