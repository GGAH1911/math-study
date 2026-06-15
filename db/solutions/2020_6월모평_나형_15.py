from sympy import symbols, limit, simplify, solve, Piecewise
x, a = symbols('x a', real=True)

def f(x_val):
    return Piecewise((-2*x_val + 3, x_val < 0), (-2*x_val + 2, True))

def g_func(x_val, a_val):
    return Piecewise((2*x_val, x_val < a_val), (2*x_val - 1, True))

a_val = 1
left_0 = limit(f(x) * g_func(x, a_val), x, 0, '-')
right_0 = limit(f(x) * g_func(x, a_val), x, 0, '+')
val_0 = f(0) * g_func(0, a_val)

left_a = limit(f(x) * g_func(x, a_val), x, a_val, '-')
right_a = limit(f(x) * g_func(x, a_val), x, a_val, '+')
val_a = f(a_val) * g_func(a_val, a_val)

if left_0 == right_0 == val_0 and left_a == right_a == val_a:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')