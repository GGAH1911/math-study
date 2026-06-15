import math
from sympy import *

c = 1 + sqrt(2)
b_sq = 2*c

# 정사각형 조건 검증
assert abs(2*c - b_sq) < 1e-10, "2c = b² 조건 불만족"
assert abs(c**2 - (1 + b_sq)) < 1e-10, "c² = 1 + b² 조건 불만족"

# 변의 길이
s = 2*c
print(f"한 변의 길이: {s} = {simplify(s)}")

# 대각선의 길이
d = s * sqrt(2)
d_simplified = simplify(d)
print(f"대각선의 길이: {d_simplified}")

# 정답 확인: 4 + 2√2
expected = 4 + 2*sqrt(2)
assert simplify(d - expected) == 0, f"답이 {expected}와 일치하지 않음"

print("VERIFY_PASS")