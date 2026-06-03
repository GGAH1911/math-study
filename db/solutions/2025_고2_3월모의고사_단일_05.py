from sympy import symbols, Eq, solve
x, k = symbols('x k')
f = lambda x_val, k_val: 2*x_val + k_val
f_inv = lambda y_val, k_val: (y_val - k_val) / 2
k_val = 3
assert f_inv(7, k_val) == 2, 'f_inv(7) != 2'
result = f(k_val, k_val)
assert result == 9, f'f(k) = {result} != 9'
print('VERIFY_PASS')