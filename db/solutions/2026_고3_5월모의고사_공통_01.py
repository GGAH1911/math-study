import sympy as sp

CANDIDATE = 4                          # ④ 4 (기존 값 유지)

# 문제: base^(1/root) * (base^k)^(1/root) 의 값
#   원문제: 2^(1/3) * 32^(1/3),  32 = 2^5  →  base=2, root=3, k=5
PARAMS = dict(base=2, root=3, k=5)


def solve(prm):
    base = sp.Integer(prm['base'])
    root = sp.Rational(prm['root'])
    k = sp.Integer(prm['k'])
    # base^(1/root) * (base^k)^(1/root) = base^((1+k)/root)
    exponent = sp.Rational(1 + k, root)
    return sp.nsimplify(base ** exponent)


def statement(prm):
    return (f"{prm['base']}^(1/{prm['root']}) \\times "
            f"\\sqrt[{prm['root']}]{{{prm['base']}^{prm['k']}}} 의 값은?")


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
