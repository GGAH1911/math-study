import math
from sympy import symbols, log, solve, simplify

x = symbols('x', real=True)

# 원래 부등식: log_3(x-3) + log_3(x+3) <= 3
# 이를 (x-3)(x+3) <= 27로 변환

# x = 4, 5, 6 검증
for val in [4, 5, 6]:
    left = math.log(val-3, 3) + math.log(val+3, 3)
    if left <= 3 + 1e-10:
        pass
    else:
        print('VERIFY_FAIL')
        exit()

# x = 3은 정의역 밖 (x > 3 필요)
# x = 7 검증 (초과 확인)
val = 7
left = math.log(val-3, 3) + math.log(val+3, 3)
if left > 3:
    pass
else:
    print('VERIFY_FAIL')
    exit()

# 정수해의 합
ans = 4 + 5 + 6
if ans == 15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')