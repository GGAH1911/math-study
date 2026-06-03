from sympy import *

a = sqrt(3)
k = Integer(5)

x_A, x_B = Integer(2), Integer(4)
y_A = a**x_A + k   # = 8
y_B = a**x_B + k   # = 14

# A, B on line y = 3x+2
assert simplify(y_A - (3*x_A + 2)) == 0, 'A not on line'
assert simplify(y_B - (3*x_B + 2)) == 0, 'B not on line'

# D = y-intercept
x_D, y_D = Integer(0), Integer(2)

# C = reflection of B about y=x
x_C, y_C = y_B, x_B   # (14, 4)

# C on y = log_a(x - k)
log_val = log(x_C - k) / log(a)
assert simplify(log_val - y_C) == 0, 'C not on log curve'

# |AB| = |AD|
AB2 = (x_B-x_A)**2 + (y_B-y_A)**2
AD2 = (x_A-x_D)**2 + (y_A-y_D)**2
assert simplify(AB2 - AD2) == 0, f'AB^2={AB2} != AD^2={AD2}'

# |BC| = |CD|
BC2 = (x_C-x_B)**2 + (y_C-y_B)**2
CD2 = (x_C-x_D)**2 + (y_C-y_D)**2
assert simplify(BC2 - CD2) == 0, f'BC^2={BC2} != CD^2={CD2}'

print(f'a = {a}, k = {k}, a*k = {simplify(a*k)}')
print('VERIFY_PASS')
