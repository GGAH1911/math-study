import sympy as sp
t, k = sp.symbols('t k')
v = 3*t**2 - 4*t + k
x = sp.integrate(v, t) + sp.Symbol('C')
x_func = lambda t_val, k_val, c_val: t_val**3 - 2*t_val**2 + k_val*t_val + c_val

C = 0
x_0 = x_func(0, k, C)
assert x_0 == 0, f'x(0)={x_0}, should be 0'

x_1_k = 1 - 2 + k
k_val = -3 - (1 - 2)
k_val = -2

x_t = lambda t_val: t_val**3 - 2*t_val**2 + (-2)*t_val
assert x_t(0) == 0, f'x(0)={x_t(0)}, should be 0'
assert x_t(1) == -3, f'x(1)={x_t(1)}, should be -3'

x_3 = x_t(3)
x_1 = x_t(1)
change = x_3 - x_1
assert change == 6, f'change={change}, should be 6'
print('VERIFY_PASS')