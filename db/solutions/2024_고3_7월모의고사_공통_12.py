import sympy as sp
from sympy import symbols, integrate, simplify

# 0 <= x < 4에서 f(x) = x^3 - 6x^2 + 12x
# 4 <= x <= 7에서 f(x) = f(x-4) + 16

x = symbols('x')

# f(u) for 0 <= u < 4
def f_base(u):
    return u**3 - 6*u**2 + 12*u

# f(x) for 0 <= x <= 7
def f_extended(x_val):
    if isinstance(x_val, (int, float)):
        if x_val < 4:
            return x_val**3 - 6*x_val**2 + 12*x_val
        else:
            return f_extended(x_val - 4) + 16
    else:
        return sp.Piecewise((x_val**3 - 6*x_val**2 + 12*x_val, x_val < 4), 
                           (f_base(x_val - 4) + 16, True))

# 적분 계산
u = symbols('u')
integral_base = integrate(u**3 - 6*u**2 + 12*u, (u, 0, 3))
integral_total = integral_base + 16*3

if simplify(integral_total - sp.Rational(273, 4)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')