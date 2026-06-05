import sympy as sp
from fractions import Fraction

# 이항분포 B(n, p)의 기댓값은 E(X) = n*p
n = 60
p = Fraction(5, 12)

expected_value = n * p
expected_value_float = float(expected_value)

print(f"n = {n}, p = {p}")
print(f"E(X) = n*p = {n} * {p} = {expected_value} = {expected_value_float}")

# 답이 25인지 확인
if expected_value == 25:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL (expected 25, got {expected_value})")