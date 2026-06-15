import sympy as sp
from sympy import cos, sin, pi, solve, symbols

x = symbols('x', real=True)

# Step 1: Solve 4cos²x - 1 = 0
eq1 = 4*cos(x)**2 - 1
sols_eq = solve(eq1, x)
print(f'Solutions to equation: {sols_eq}')

# Step 2: Filter for 0 < x < 2π
sols_in_range = []
for sol in sols_eq:
    for k in range(-2, 3):
        candidate = sol + 2*pi*k
        if 0 < candidate < 2*pi:
            sols_in_range.append(float(candidate))

sols_in_range = sorted(list(set([round(s, 10) for s in sols_in_range])))
print(f'Solutions in (0, 2π): {sols_in_range}')

# Step 3: Check sin(x)*cos(x) < 0 for each solution
valid_sols = []
for x_val in sols_in_range:
    sin_val = sin(x_val)
    cos_val = cos(x_val)
    product = sin_val * cos_val
    if float(product) < -1e-10:  # sin(x)*cos(x) < 0
        valid_sols.append(x_val)
        print(f'x = {x_val:.6f}: sin(x)*cos(x) = {float(product):.6f} < 0 ✓')
    else:
        print(f'x = {x_val:.6f}: sin(x)*cos(x) = {float(product):.6f} ✗')

# Step 4: Sum all valid solutions
total_sum = sum(valid_sols)
print(f'\nValid solutions: {valid_sols}')
print(f'Sum of all x: {total_sum:.10f}')

# Express as a multiple of π
sum_over_pi = total_sum / float(pi)
print(f'Sum / π = {sum_over_pi:.10f}')

# Expected answer: 7π/3
expected = 7 * float(pi) / 3
if abs(total_sum - expected) < 1e-9:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')