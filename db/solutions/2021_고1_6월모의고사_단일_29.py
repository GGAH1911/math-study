import sympy as sp
from sympy import symbols, solve, sqrt

x, m = symbols('x m', real=True)

# Check m=2
m_val = 2
print(f'Checking m = {m_val}:')

# Left: x^2 + (2-m)x - 5 = 0
left_eq = x**2 + (2-m_val)*x - 5
left_roots = solve(left_eq, x)
print(f'Left roots: {left_roots}')
left_in_range = [r for r in left_roots if r <= -2]
print(f'Left roots in [-inf, -2]: {left_in_range}')

# Right: same equation
right_roots = left_roots
right_in_range = [r for r in right_roots if r >= 1]
print(f'Right roots in [1, inf]: {right_in_range}')

# Middle: x^2 + mx + 1 = 0
mid_eq = x**2 + m_val*x + 1
mid_roots = solve(mid_eq, x)
print(f'Middle roots: {mid_roots}')
mid_in_range = [r for r in mid_roots if -2 < r < 1]
print(f'Middle roots in (-2, 1): {mid_in_range}')

total_m2 = len(left_in_range) + len(mid_in_range) + len(right_in_range)
print(f'Total intersections for m=2: {total_m2}\n')

# Check m=2.5
m_val = 2.5
print(f'Checking m = {m_val}:')
left_eq = x**2 + (2-m_val)*x - 5
left_roots = solve(left_eq, x)
print(f'Left roots: {left_roots}')
left_in_range = [r for r in left_roots if r <= -2]
print(f'Left roots in [-inf, -2]: {left_in_range}')

right_in_range = [r for r in left_roots if r >= 1]
print(f'Right roots in [1, inf]: {right_in_range}')

mid_eq = x**2 + m_val*x + 1
mid_roots = solve(mid_eq, x)
print(f'Middle roots: {mid_roots}')
mid_in_range = [r for r in mid_roots if -2 < r < 1]
print(f'Middle roots in (-2, 1): {mid_in_range}')

total_m25 = len(left_in_range) + len(mid_in_range) + len(right_in_range)
print(f'Total intersections for m=2.5: {total_m25}\n')

if total_m2 == 3 and total_m25 == 3:
    S = 2 + 2.5
    result = 10 * S
    print(f'S = {S}')
    print(f'10S = {result}')
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')