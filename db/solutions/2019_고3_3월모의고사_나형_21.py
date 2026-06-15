import sympy as sp
from sympy import sqrt, symbols, diff, solve, simplify

p = symbols('p', real=True, positive=True)

# c(p) = (2√p - p + 2)/2
c = (2*sqrt(p) - p + 2) / 2

# c(p) - 8
diff_c = c - 8
print(f"c(p) - 8 = {diff_c}")

# Simplify
numerator = 2*sqrt(p) - p - 14
print(f"Numerator: {numerator}")

# Find critical points
derivative = diff(numerator, p)
print(f"Derivative: {derivative}")

critical_points = solve(derivative, p)
print(f"Critical points: {critical_points}")

# Evaluate at p=1
value_at_1 = numerator.subs(p, 1)
print(f"Value at p=1: {value_at_1}")

# Distance formula
# d = |numerator|/(2√2)
min_distance = sp.Abs(value_at_1) / (2*sqrt(2))
min_distance_simplified = simplify(min_distance)
print(f"Minimum distance = {min_distance_simplified}")
print(f"Rationalized = {simplify(min_distance_simplified * sqrt(2) / sqrt(2))}")

if simplify(min_distance_simplified - 13*sqrt(2)/4) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')