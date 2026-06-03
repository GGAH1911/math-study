import sympy as sp
import numpy as np

x = sp.Symbol('x')
solutions = []

for beta_val in [-4, 4]:
    a_coef = -beta_val - 2
    b_coef = -2 * a_coef - 4
    f_expr = x**4 + a_coef * x**3 + b_coef * x**2 + x
    f_lam = sp.lambdify(x, f_expr, 'numpy')

    # f의 원래 조건 검증
    assert f_expr.subs(x, 0) == 0
    assert sp.limit(f_expr / x, x, 0) == 1
    assert f_expr.subs(x, 2) == 2
    assert f_expr.subs(x, beta_val) == beta_val
    assert sp.diff(f_expr, x).subs(x, 2) != 1

    if beta_val == -4:
        def g(y, f_lam=f_lam):
            if y <= -4 or y >= 2:
                return float(y)
            return float(f_lam(y))
    else:
        def g(y, f_lam=f_lam):
            if y <= 2 or y >= 4:
                return float(y)
            return float(f_lam(y))

    # 원래 제약: {g(x)-x}{g(x)-f(x)} = 0
    for y_test in np.linspace(-6, 6, 200):
        gy = g(y_test)
        fy = float(f_lam(y_test))
        assert abs((gy - y_test) * (gy - fy)) < 1e-7

    # 연속성
    for c in [-4, 0, 2, 4]:
        assert abs(g(c - 1e-7) - g(c + 1e-7)) < 1e-3

    # 조건 (가): x=2에서 좌우 도함수 불일치
    h = 1e-5
    left = (g(2) - g(2 - h)) / h
    right = (g(2 + h) - g(2)) / h
    assert abs(left - right) > 0.1

    # 조건 (나)(i): x>=4 대칭
    for xt in np.linspace(4, 10, 40):
        assert abs(g(-xt) + g(xt)) < 1e-6

    # 조건 (나)(ii): 임계값이 정확히 4 (4 바로 아래에서 깨짐)
    breaks = any(abs(g(-xt) + g(xt)) > 1e-3 for xt in np.linspace(2.1, 3.99, 40))
    assert breaks

    solutions.append(g(-2) / g(3))

total = sum(solutions)
if abs(total - (-11)) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
