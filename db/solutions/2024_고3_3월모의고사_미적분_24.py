import sympy as sp
n = sp.symbols('n', positive=True)
# 원래 조건을 만족하는 구체적 수열 예시 a_n=1/n, b_n=3n 으로 검증
for a_expr, b_expr in [(1/n, 3*n), (1/n + 1/n**2, 3*n + sp.sqrt(n)), (1/n - 2/n**3, 3*n - 5)]:
    lim_na = sp.limit(n*a_expr, n, sp.oo)
    lim_bn = sp.limit(b_expr/n, n, sp.oo)
    assert lim_na == 1 and lim_bn == 3
    val = sp.limit((n**2*a_expr + b_expr)/(1 + 2*b_expr), n, sp.oo)
    if val != sp.Rational(2,3):
        print('VERIFY_FAIL'); break
else:
    print('VERIFY_PASS')
