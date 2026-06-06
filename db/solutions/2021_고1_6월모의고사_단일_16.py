from sympy import symbols, div, Poly, expand, factor

x = symbols('x')
f = x**3 - 3*x**2 + 2*x

# (가) f(0)=0
assert f.subs(x, 0) == 0, 'VERIFY_FAIL: f(0) != 0'

# (나) f(x)를 (x-2)^2으로 나눈 나머지가 2(x-2)
divisor = (x - 2)**2
quot, rem = div(Poly(f, x), Poly(divisor, x), x)
rem_expr = rem.as_expr()
expected_rem = 2*(x - 2)
assert expand(rem_expr - expected_rem) == 0, f'VERIFY_FAIL: remainder {rem_expr} != 2(x-2)'

# Q(x) = quotient of f(x)/(x-1)
q, r = div(Poly(f, x), Poly(x - 1, x), x)
assert r.as_expr() == 0, 'VERIFY_FAIL: remainder of f/(x-1) != 0'
Q = q.as_expr()
Q5 = Q.subs(x, 5)
assert Q5 == 15, f'VERIFY_FAIL: Q(5)={Q5} != 15'

print('VERIFY_PASS')
