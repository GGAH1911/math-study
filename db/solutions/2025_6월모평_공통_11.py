from sympy import symbols, solve, simplify
x = symbols('x')
f = lambda x_val: x_val**3 - 2*x_val**2 - 4*x_val
f_prime = lambda x_val: 3*x_val**2 - 4*x_val - 4

# 검증
assert f(0) == 0, 'f(0) should be 0'
assert f(-1) == 1, 'f(-1) should be 1'
assert f_prime(-1) == 3, 'f\'(-1) should be 3'
assert -3*(-1) + 1 == 4, 'y-intercept should be 4'
result = f(1)
assert result == -5, f'f(1) should be -5, got {result}'
print('VERIFY_PASS')