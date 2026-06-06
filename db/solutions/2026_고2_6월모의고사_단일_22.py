import sympy as sp
from sympy import cbrt, simplify, Rational

# 원래 문제: ³√49 × ³√7⁴
a = cbrt(49)
b = cbrt(7**4)
result = a * b
result_simplified = simplify(result)

# 직접 계산으로도 확인
# 49 = 7^2 이므로 ³√49 = 7^(2/3)
# ³√7^4 = 7^(4/3)
# 따라서 7^(2/3) × 7^(4/3) = 7^(6/3) = 7^2 = 49

answer = 49
if result_simplified == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')