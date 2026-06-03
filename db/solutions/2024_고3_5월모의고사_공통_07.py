from sympy import symbols, expand, factor, simplify

x = symbols('x')
# f(x) = x^3 - 3x^2 + 3x + 2
def f(t):
    return t**3 - 3*t**2 + 3*t + 2

def f_prime(t):
    return 3*t**2 - 6*t + 3

# 조건 1: f'(x) = {3x - f(1)}(x-1)
f1 = f(1)
lhs = f_prime(x)
rhs = (3*x - f1)*(x - 1)
diff = simplify(expand(lhs) - expand(rhs))
assert diff == 0, f'f prime mismatch: {diff}'

# 조건 2: f'(x) >= 0 for all x (실수 전체에서 증가)
import numpy as np
test_vals = np.linspace(-100, 100, 10000)
fp_vals = 3*test_vals**2 - 6*test_vals + 3
assert np.all(fp_vals >= 0), 'f is not globally increasing'

# 조건 3: f(2) == 4
result = f(2)
assert result == 4, f'f(2) = {result}, expected 4'

print('VERIFY_PASS')
