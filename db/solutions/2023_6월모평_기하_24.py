import sympy as sp
from sympy import sqrt, symbols, simplify

# 주어진 조건
# 주축의 길이 = 6 → a = 3
# 점근선 y = 2x → b/a = 2

a = 3
b = 6

# 쌍곡선: x²/a² - y²/b² = 1
# 점근선 확인
asymptote_slope = b / a
assert asymptote_slope == 2, f"Asymptote slope is {asymptote_slope}, expected 2"

# 초점까지의 거리
c_squared = a**2 + b**2
c = sqrt(c_squared)
distance = 2 * c

# 검증
expected = 6 * sqrt(5)
assert simplify(distance - expected) == 0, f"Distance {distance} != {expected}"

print('VERIFY_PASS')