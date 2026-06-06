from sympy import symbols, Rational, summation, simplify, solve, Abs
import numpy as np

# 공비 설정
r = Rational(-1, 2)
s = Rational(1, 4)

# 조건 2 검증: 1/r + 1/s = 2
check2 = 1/r + 1/s
print(f'Condition 2: 1/r + 1/s = {check2} (should be 2)')
assert check2 == 2, 'Condition 2 failed'

# 조건 3 검증: 3*sum|a_{2n}| = 7*sum|a_{3n}|
# |a_{2n}| = |a_1| * |r|^{2n-1}
# sum|a_{2n}| = |a_1| * |r| / (1 - |r|^2)
sum_a2n = Abs(r) / (1 - Abs(r)**2)
sum_a3n = Abs(r)**2 / (1 - Abs(r)**3)
check3_left = 3 * sum_a2n
check3_right = 7 * sum_a3n
print(f'Condition 3 left: {simplify(check3_left)}')
print(f'Condition 3 right: {simplify(check3_right)}')
assert simplify(check3_left - check3_right) == 0, 'Condition 3 failed'

# S 계산
# S = sum_{n=1}^∞ [(1/4)^{n-1} + (1/4)^{2n+1}]
part1 = 1 / (1 - s)  # sum (1/4)^{n-1}
part2 = (s**3) / (1 - s**2)  # sum (1/4)^{2n+1}
S = part1 + part2
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
print(f'S = {S}')

result = 120 * S
print(f'120S = {result}')
assert result == 162, f'Expected 162, got {result}'
print('VERIFY_PASS')