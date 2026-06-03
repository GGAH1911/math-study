import math

# Given: p = 16/3
p = 16/3

# Point P in first quadrant intersection
x0, y0 = 12, 16

# Check P is on parabola x^2 = 8(y+2)
assert abs(x0**2 - 8*(y0+2)) < 1e-9, 'P not on first parabola'

# Check P is on parabola y^2 = 4px
assert abs(y0**2 - 4*p*x0) < 1e-9, 'P not on second parabola'

# Check x0 > 0 and y0 > 0 (first quadrant)
assert x0 > 0 and y0 > 0, 'P not in first quadrant'

# Focus F of x^2=8(y+2): vertex (0,-2), a=2 => F=(0,0)
F = (0, 0)

# Directrix of x^2=8(y+2): y = -4
directrix_y = -4

# PH: perpendicular distance from P to directrix y=-4
PH = y0 - directrix_y

# PF: distance from P to focus F
PF = math.sqrt((x0 - F[0])**2 + (y0 - F[1])**2)

# Verify PF == PH (focus-directrix property)
assert abs(PF - PH) < 1e-9, f'Focus-directrix property failed: PF={PF}, PH={PH}'

# Verify PH + PF = 40
total = PH + PF
assert abs(total - 40) < 1e-9, f'PH+PF={total} != 40'

print(f'p = {p} = 16/3, PH = {PH}, PF = {PF}, PH+PF = {total}')
print('VERIFY_PASS')