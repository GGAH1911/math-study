import sympy as sp
x = sp.Symbol('x')
a, b, k = 2, 6, 4
def f(x_val):
    if x_val < a:
        if x_val < -3:
            return -x_val - 4
        else:
            return x_val + 2
    elif x_val < b:
        return x_val - 10
    else:
        if x_val < 9:
            return -x_val + 8
        else:
            return x_val - 10
f_a = f(a)
f_b = f(b)
f_k = f(k)
result = f_a * f_b * f_k
assert f_k < 0, f'f(k)={f_k} should be < 0'
assert result == 96, f'Expected 96, got {result}'
print('VERIFY_PASS')