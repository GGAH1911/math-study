import sympy as sp
from sympy import sqrt, simplify

# 검증
a_val = 2*sqrt(3)

# |AH| 계산
AH = a_val * (1 + sqrt(3)) / 2

# |FH| 계산
FH = a_val * (3 + sqrt(3)) / 2

# 타원의 장축
tau_ellipse = AH + FH
print(f"2a' = {simplify(tau_ellipse)}")

# 조건 검증
result = tau_ellipse + 2*a_val
print(f"2a' + 2a = {simplify(result)}")
print(f"Expected: 6 + 8√3 = {6 + 8*sqrt(3)}")

if simplify(result - (6 + 8*sqrt(3))) == 0:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")