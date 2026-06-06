from sympy import symbols, Rational, expand
x = symbols('x')
f = x**3 - Rational(5,2)*x**2 + 2*x - Rational(1,2)
g = 2*x - Rational(1,2)

# 조건 검증
assert f.subs(x, 0) == g.subs(x, 0), 'h(0) condition failed'
assert (f + g).subs(x, 2) == 5, 'h(2) condition failed'

# h(4) 계산
h_4 = (f + g).subs(x, 4)
assert h_4 == 39, f'h(4) = {h_4}, expected 39'
print('VERIFY_PASS')