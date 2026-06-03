import sympy as sp

x = sp.Symbol('x')

# 원래 문제에서 유도된 g(x), f(x)
g = 4*x**2 + 12*x - 6
f = x * sp.diff(g, x)  # 조건 (나): f(x) = x g'(x)

# 조건 (가) 검증: 좌변 - 우변 = 0 이어야 함
lhs = sp.integrate(x*f, (x, 1, x)) + sp.integrate(x*g, (x, -1, x))
rhs = 3*x**4 + 8*x**3 - 3*x**2
diff_ga = sp.simplify(sp.expand(lhs) - rhs)

# 조건 (나) 검증: f(x) = x g'(x)
diff_na = sp.simplify(f - x*sp.diff(g, x))

# 정적분 계산
result = sp.integrate(g, (x, 0, 3))

if diff_ga == 0 and diff_na == 0 and result == 72:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: (가)잔차={diff_ga}, (나)잔차={diff_na}, 적분값={result}')
