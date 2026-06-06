import sympy as sp
from sympy import symbols, solve, Abs

x = symbols('x')

# Verify the quadratic inequality solution
quadratic = x**2 - 14*x + 40
roots = solve(quadratic, x)
print(f'Roots of x^2 - 14x + 40: {roots}')
# Should be [4, 10]

# Check each value of n
for n in [6, 7, 8]:
    # Count natural numbers x in [4, 10] satisfying |x - n| > 2
    count = 0
    solutions = []
    for x_val in range(4, 11):
        if abs(x_val - n) > 2 and 4 <= x_val <= 10:
            count += 1
            solutions.append(x_val)
    print(f'n={n}: natural numbers satisfying both conditions: {solutions}, count={count}')

# Verify sum
valid_n = [6, 7, 8]
total = sum(valid_n)
print(f'\nSum of all valid n values: {total}')
if total == 21:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')