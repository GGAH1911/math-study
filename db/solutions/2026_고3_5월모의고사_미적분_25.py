import sympy as sp
import numpy as np
from sympy import sin, cos, limit, symbols, simplify

t = symbols('t', real=True, positive=True)

# Point P on the curve y = sin(2x)
P_x = t
P_y = sin(2*t)

# Slope of OP
slope_OP = P_y / P_x  # sin(2t) / t

# Slope of perpendicular line to OP
slope_perp = -P_x / P_y  # -t / sin(2t)

# Line through P perpendicular to OP: y - P_y = slope_perp * (x - P_x)
# At y = 0: -P_y = slope_perp * (x - P_x)
# -sin(2t) = -t/sin(2t) * (x - t)
# sin^2(2t) = t(x - t)
# x = t + sin^2(2t) / t

OQ = t + sin(2*t)**2 / t

# Calculate the limit
ratio = OQ / t
result = limit(ratio, t, 0, '+')

print(f'OQ/t = {simplify(ratio)}')
print(f'lim (t→0+) OQ/t = {result}')

if result == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')