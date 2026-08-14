# log_b(x+a) ≤ k + log_{1/b}(x-c) 를 만족하는 정수 x 의 합.
# 밑변환 log_{1/b}(x-c) = -log_b(x-c) → log_b((x+a)(x-c)) ≤ k → (x+a)(x-c) ≤ b^k.
# ★진수조건 x+a>0, x-c>0 (즉 x > max(-a, c)) 를 반드시 함께 건다 — 빠뜨리면 음수 정수가 딸려 온다.
# 파라미터화: 밑 base, 두 진수의 상수항 a·c, 우변 상수 k 만 바꾸면 같은 유형의 새 문제가 된다.
CANDIDATE = 12
import sympy as sp

PARAMS = dict(base=3, a=4, c=2, k=3)   # log_3(x+4) ≤ 3 + log_{1/3}(x-2)


def _int_solutions(prm):
    """원식(로그부등식)을 정의역 위에서 직접 판정해 정수해 목록을 만든다."""
    b = sp.Integer(prm['base'])
    a = sp.Integer(prm['a'])
    c = sp.Integer(prm['c'])
    k = sp.Integer(prm['k'])
    x = sp.symbols('x', real=True)

    # 원식 그대로: 좌변 - 우변 ≤ 0 이면 만족
    gap = sp.log(x + a, b) - (k + sp.log(x - c, sp.Rational(1, 1) / b))

    lo = max(-a, c)                                  # 진수조건: x > lo
    # 상한: (x+a)(x-c) = b^k 의 큰 근 (증가구간이므로 그 위로는 항상 위배)
    roots = sp.solve(sp.Eq(sp.expand((x + a) * (x - c)), b ** k), x)
    hi = max(sp.re(sp.nsimplify(r)) for r in roots)

    ints = []
    n = int(sp.floor(lo)) + 1
    last = int(sp.floor(hi)) + 2
    while n <= last:
        if n > lo:                                   # 진수조건 재확인(정수 경계 안전)
            g = gap.subs(x, sp.Integer(n))
            val = sp.N(g)
            if val.is_real:
                if val < -1e-9:
                    ints.append(n)
                elif val <= 1e-9 and sp.simplify(g) <= 0:   # 등호 경계는 정확히 판정
                    ints.append(n)
        n += 1
    return ints


def solve(prm):
    return sp.Integer(sum(_int_solutions(prm)))


def statement(prm):
    b, a, c, k = prm['base'], prm['a'], prm['c'], prm['k']
    return (f"부등식 log_{{{b}}}(x+{a}) ≤ {k} + log_{{1/{b}}}(x-{c}) 를 "
            f"만족시키는 모든 정수 x 의 값의 합을 구하시오.")


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
