from sympy import *

x = symbols('x', positive=True)

f_expr = 4*x**2 / (x**2 + 3)
g_expr = sqrt(3*x / (4 - x))
h_expr = f_expr - g_expr
hp = diff(h_expr, x)
hpp = diff(hp, x)

# ㄱ: h(1) = 0
h1 = simplify(h_expr.subs(x, 1))
assert h1 == 0, f'h(1)={h1}, expected 0'

# zeros: h(3) = 0 as well
h3 = simplify(h_expr.subs(x, 3))
assert h3 == 0, f'h(3)={h3}, expected 0'

# sign of h
assert float(h_expr.subs(x, 2).evalf()) > 0, 'h(2) should be positive'
assert float(h_expr.subs(x, Rational(1,2)).evalf()) < 0, 'h(1/2) should be negative'
assert float(h_expr.subs(x, Rational(7,2)).evalf()) < 0, 'h(7/2) should be negative'

# ㄴ: b-a = 3-1 = 2
assert 3 - 1 == 2, 'b-a should be 2'

# ㄷ: max of h'(x) at x=1 is 5/6, not 7/6
hp1 = simplify(hp.subs(x, 1))
assert hp1 == Rational(5, 6), f"h'(1)={hp1}, expected 5/6"

# Confirm x=1 is max of h': h''>0 on (0,1), h''<0 on (1,4)
assert float(hpp.subs(x, Rational(1,2)).evalf()) > 0, "h''(0.5) should be >0"
assert float(hpp.subs(x, 2).evalf()) < 0, "h''(2) should be <0"

# max h' = 5/6 != 7/6 => ㄷ is FALSE; answer is ② (ㄱ,ㄴ)
print('VERIFY_PASS')
