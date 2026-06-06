import sympy as sp
x = sp.Symbol('x')
f = 2*x + 3/x
g = 2*x + 3/x + 9
f_at_2 = f.subs(x, 2)
g_at_minus2 = g.subs(x, -2)
result = f_at_2 + g_at_minus2
g_at_minus3 = g.subs(x, -3)
print('f(2) =', f_at_2)
print('g(-2) =', g_at_minus2)
print('f(2) + g(-2) =', result)
print('g(-3) =', g_at_minus3)
assert result == 9, f'조건 (나) 검증 실패: {result} != 9'
assert g_at_minus3 == 2, f'답 검증 실패: {g_at_minus3} != 2'
print('VERIFY_PASS')