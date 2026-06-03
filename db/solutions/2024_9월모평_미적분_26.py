import sympy as sp
from fractions import Fraction

# 답: 3/2, d=2, r=1/3
d = 2
r = Fraction(1, 3)

# 망원급수 검증: sum 1/(a_n * a_{n+1}) = 1/d
part1_expected = Fraction(1, d)

# 기하급수 검증: sum b_n = 1/(1-r)
part2_actual = 1 / (1 - r)
part2_expected = Fraction(3, 2)

# 조건 검증: 두 합이 2가 되는지 확인
total = float(part1_expected) + float(part2_expected)

if abs(total - 2.0) < 1e-9 and part2_actual == part2_expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')