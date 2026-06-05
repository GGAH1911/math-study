from sympy import symbols, expand
x = symbols('x')
# P(x) = x^2 + 2x + 1
P = lambda t: t**2 + 2*t + 1
# Check condition P(x+1) - P(x) = 2x + 3
for test_x in [0, 1, 2, -1]:
    diff = P(test_x + 1) - P(test_x)
    expected = 2*test_x + 3
    assert diff == expected, f'Failed at x={test_x}'
# Check initial condition P(0) = 1
assert P(0) == 1, 'P(0) != 1'
# Verify answer: P(2) = 9
assert P(2) == 9, 'P(2) != 9'
print('VERIFY_PASS')