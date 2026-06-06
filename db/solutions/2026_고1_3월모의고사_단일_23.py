import sympy as sp
import math

# 원래 식: sqrt(3) + sqrt(12) = sqrt(n)
left_side = sp.sqrt(3) + sp.sqrt(12)
n = 27
right_side = sp.sqrt(n)

# 두 변이 같은지 확인
if sp.simplify(left_side - right_side) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')