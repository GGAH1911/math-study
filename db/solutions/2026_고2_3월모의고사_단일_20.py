import sympy as sp
x = sp.Symbol('x')
f = (x-1)*(x-5)
g = (x-2)*(x-1)
h = (x-5)*(x-2)
q = (x-1)
r = (x-2)
# 조건 (가) 검증: f*g = (x-1)*h*q
lhs_1 = sp.expand(f*g)
rhs_1 = sp.expand((x-1)*h*q)
assert lhs_1 == rhs_1, f'조건 (가) 실패'
# 조건 (나) 검증: g*h = (x-2)*f*r
lhs_2 = sp.expand(g*h)
rhs_2 = sp.expand((x-2)*f*r)
assert lhs_2 == rhs_2, f'조건 (나) 실패'
# f(-1) + g(-1) = 18 검증
f_minus1 = f.subs(x, -1)
g_minus1 = g.subs(x, -1)
assert f_minus1 + g_minus1 == 18, f'조건 검증 실패'
# h(0) = 10 검증
h_0 = h.subs(x, 0)
assert h_0 == 10, f'h(0) 검증 실패: {h_0}'
print('VERIFY_PASS')