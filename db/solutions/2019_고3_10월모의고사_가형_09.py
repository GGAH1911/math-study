from sympy import symbols, integrate, Function

x = symbols('x')

# Given: integral of f from 3 to 5 equals 36
# We need integral of f(2x+1) from x=1 to x=2
# Substitution: u = 2x+1, du = 2dx
# When x=1, u=3; when x=2, u=5
# So integral = (1/2) * integral of f(u) from 3 to 5 = (1/2)*36 = 18

result = 36 / 2  # = 18

expected = 18
if abs(result - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
