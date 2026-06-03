from sympy import symbols, diff, solve
x = symbols('x')
a_val = 3
f = x**3 + a_val*x**2 + 3*a_val
fp = diff(f, x)
# x=-2에서 극대 조건 확인
assert fp.subs(x, -2) == 0, 'f prime at x=-2 should be 0'
# 극소점 x=0 확인
critical = solve(fp, x)
assert 0 in critical, '0 should be a critical point'
assert -2 in critical, '-2 should be a critical point'
fpp = diff(fp, x)
assert fpp.subs(x, -2) < 0, 'x=-2 should be local max'
assert fpp.subs(x, 0) > 0, 'x=0 should be local min'
min_val = f.subs(x, 0)
if min_val == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')