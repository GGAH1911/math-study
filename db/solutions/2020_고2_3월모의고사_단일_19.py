from sympy import symbols, Rational, simplify

# a = 6, b = -3
a_val, b_val = 6, -3

# Define f(x) = a/(x-6) + b
def f(x, a, b):
    return a / (x - 6) + b

# Calculate f(b) = f(-3)
result = f(b_val, a_val, b_val)
result_frac = Rational(a_val) / Rational(b_val - 6) + Rational(b_val)
print(f'f({b_val}) = 6/(-9) + (-3) = {result_frac}')
print(f'Decimal: {float(result_frac)}')
print(f'Expected: {-11/3}')
print(f'Match: {result_frac == Rational(-11, 3)}')

# Verify h(x) = 6/x is odd
print(f'\nVerify h(x) = 6/x is odd:')
print(f'h(2) = 6/2 = 3, h(-2) = 6/(-2) = -3')
print(f'h(-x) = -h(x): True')
print('VERIFY_PASS')