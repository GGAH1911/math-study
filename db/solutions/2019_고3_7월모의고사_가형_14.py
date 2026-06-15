import sympy as sp
from sympy import ln, integrate, symbols, atan

x = symbols('x')
f = (2*x - 2)/(x**2 - 2*x + 2)

# Area A: integral from 0 to 1
A = -integrate(f, (x, 0, 1))
print(f'Area A = {A} = {sp.simplify(A)}')

# Area B: integral from 1 to 3
B = integrate(f, (x, 1, 3))
print(f'Area B = {B} = {sp.simplify(B)}')

# Total area
total = A + B
total_simplified = sp.simplify(total)
print(f'Total A + B = {total} = {total_simplified}')

# Numerical verification
total_numerical = float(total_simplified.evalf())
target_ln10 = float(ln(10).evalf())
print(f'Numerical check: {total_numerical} ≈ ln(10) = {target_ln10}')
print(f'Match: {abs(total_numerical - target_ln10) < 1e-10}')

# Verify total equals ln(10)
if sp.simplify(total_simplified - ln(10)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')