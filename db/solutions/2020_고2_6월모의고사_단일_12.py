import sympy as sp

# 원래 부등식: 4^x - 10*2^x + 16 <= 0
# y = 2^x 치환: y^2 - 10*y + 16 <= 0
y = sp.Symbol('y')
eq = y**2 - 10*y + 16
roots = sp.solve(eq, y)
assert roots == [2, 8], f'Expected roots [2, 8], got {roots}'

# 부등식의 해: 2 <= y <= 8
# y = 2^x이므로: 2 <= 2^x <= 8 => 1 <= x <= 3

# 자연수 x에 대해 원부등식 검증
x_vals = [1, 2, 3]
valid = []
for x_val in x_vals:
    result = 4**x_val - 10*(2**x_val) + 16
    if result <= 0:
        valid.append(x_val)

total = sum(valid)
assert valid == [1, 2, 3], f'Expected [1, 2, 3], got {valid}'
assert total == 6, f'Expected sum 6, got {total}'
print('VERIFY_PASS')