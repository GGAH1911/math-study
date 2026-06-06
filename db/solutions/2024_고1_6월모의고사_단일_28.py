import sympy as sp
x = sp.Symbol('x')
f = 2*x**2 - 4*x + 4
g = -2*x + 4

# 검증: f(x)g(x) = (f(x)-2x^2)(x^2-3x+3) + (f(x)+xg(x))
fg = sp.expand(f * g)
quotient = x**2 - 3*x + 3
remainder = f + x*g
divisor = f - 2*x**2

right = sp.expand(divisor * quotient + remainder)

if sp.expand(fg - right) == 0:
    result = f.subs(x, -2)
    if result == 20:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')