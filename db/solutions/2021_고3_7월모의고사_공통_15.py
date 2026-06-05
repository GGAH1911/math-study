import sympy as sp
x = sp.Symbol('x')
f = x**4 - 10*x**2 + 9
f_prime = 4*x**3 - 20*x

# 조건 (나) 검증
alpha = -sp.sqrt(5)
result_na = f.subs(x, alpha)
print(f'f(α) = {result_na}, 조건: -16')
assert result_na == -16, 'Condition (나) failed'

# 조건 (가) 검증
eq = f - 9
roots = sp.solve(eq, x)
real_roots = [r for r in roots if r.is_real]
print(f'f(x)=9의 실근: {real_roots}, 개수: {len(real_roots)}')
assert len(real_roots) == 3, 'Condition (가) failed'

# 적분 계산
f_0 = f.subs(x, 0)
f_sqrt5 = f.subs(x, sp.sqrt(5))
integral_val = -2 * (f_sqrt5 - f_0)
print(f'∫₀¹⁰ g(x)dx = -2[f(√5) - f(0)] = -2[{f_sqrt5} - {f_0}] = {integral_val}')
assert integral_val == 50, 'Integration failed'
print('VERIFY_PASS')