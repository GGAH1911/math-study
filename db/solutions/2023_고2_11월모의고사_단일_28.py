import sympy as sp
x = sp.Symbol('x')
f = 2*x
g = x**2 + x**3

# 조건 (나) 검증: x→0
limit_na = sp.limit(f * g**2 / x**5, x, 0)
print(f'조건(나) 극한값: {limit_na}', 'PASS' if limit_na == 2 else 'FAIL')

# 조건 (가) 검증: x→∞
limit_ga = sp.limit(f**2 * g / x**5, x, sp.oo)
print(f'조건(가) 극한값: {limit_ga}', 'PASS' if limit_ga == 4 else 'FAIL')

if limit_na == 2 and limit_ga == 4:
    answer = f.subs(x, 2) + g.subs(x, 2)
    print(f'f(2) + g(2) = {answer}')
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')