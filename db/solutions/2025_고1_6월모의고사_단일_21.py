from sympy import *

def verify():
    x = symbols('x')
    results = []

    for beta_val in [3, 4]:
        alpha_val = beta_val - 2
        k_val = 2 * beta_val

        # f(x) = (1/2)(x - beta)^2 + beta
        f = Rational(1, 2) * (x - beta_val)**2 + beta_val

        # 조건 (가): f(beta) = beta
        assert f.subs(x, beta_val) == beta_val, f'beta={beta_val}: f(beta)!=beta'

        # 조건 (나): 최솟값이 beta (꼭짓점에서 확인)
        min_val = f.subs(x, beta_val)
        assert min_val == beta_val, f'beta={beta_val}: min != beta'

        # alpha, beta가 f(x)+x=k의 근인지 확인
        eq = f + x - k_val
        roots = solve(eq, x)
        assert set(roots) == {alpha_val, beta_val}, f'beta={beta_val}: roots mismatch {roots}'

        # f(0) <= alpha + beta + f(alpha)
        f0 = f.subs(x, 0)
        fa = f.subs(x, alpha_val)
        assert f0 <= alpha_val + beta_val + fa, f'beta={beta_val}: f(0) condition failed'

        f6 = f.subs(x, 6)
        results.append(f6)

    product = results[0] * results[1]
    if product == 45:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: product={product}')

verify()
