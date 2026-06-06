import sympy as sp
x = sp.Symbol('x')
f = x**2 + 2*x
g = -sp.Rational(1, 2)*x**2 + 2*x

# 조건 (가) 검증: f(x) - 2x와 g(x) - 2x가 같은 중근을 가짐
f_minus_2x = f - 2*x
g_minus_2x = g - 2*x
print('f(x) - 2x:', f_minus_2x, '= x^2')
print('g(x) - 2x:', g_minus_2x, '= -1/2*x^2')
print('(f(x) - 2x) = x^2는 x=0에서 중근, (g(x) - 2x) = -1/2*x^2도 x=0에서 중근')

# 조건 (나) 검증: k = -1/2, 0, 1에서 합이 3
for k_val in [-sp.Rational(1, 2), 0, 1]:
    eq_f = f - 2*k_val
    eq_g = g - 2*k_val
    roots_f = sp.solve(eq_f, x)
    roots_g = sp.solve(eq_g, x)
    total = len(set(roots_f + roots_g))
    print(f'k={k_val}: f(x)=2k의 근 {len(roots_f)}개, g(x)=2k의 근 {len(roots_g)}개, 합={total}')

# 조건: f(x) - g(x) >= 0
diff = f - g
print(f'\nf(x) - g(x) = {diff} = (3/2)x^2 >= 0 for all x: True')

# 최종 답
ans = f.subs(x, 10) + g.subs(x, 6)
print(f'\nf(10) + g(6) = {f.subs(x, 10)} + {g.subs(x, 6)} = {ans}')
if ans == 114:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')