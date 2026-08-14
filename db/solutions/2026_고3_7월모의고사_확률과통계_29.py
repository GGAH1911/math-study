# 1..2n+1 이 적힌 공에서 2개를 꺼내, 홀·짝 하나씩이면 그 짝수를, 아니면 0 을 기록 → X.
# E(X^2)=k·E(X) 조건으로 n 을 정하고 E(pX+q) 를 구한다.
#
# ★파라미터화 솔버(scripts/CLAUDE.md 규격): PARAMS 를 바꾸면 같은 유형의 새 문제와
#   검증된 답이 그대로 나온다. 원문제는 PARAMS 기본값으로 재현된다.
CANDIDATE = 41
import sympy as sp

PARAMS = dict(k=14, p=7, q=sp.Rational(2, 3))     # E(X^2)=k E(X), 구하는 값 E(pX+q)


def solve(prm):
    """조건 E(X^2)=k·E(X) 로 n 을 정하고 E(pX+q) 를 돌려준다."""
    n = sp.symbols('n', positive=True, integer=True)
    j = sp.symbols('j', positive=True, integer=True)

    # 공 2n+1 개 중 홀수 n+1 개, 짝수 n 개. 짝수 2j 를 기록 = 그 짝수 1개 + 홀수 1개.
    tot = sp.binomial(2*n + 1, 2)                  # 두 공을 뽑는 경우의 수
    w = (n + 1)/tot                                # P(X = 2j), j = 1..n
    EX = sp.simplify(sp.summation(2*j*w, (j, 1, n)))
    EX2 = sp.simplify(sp.summation((2*j)**2*w, (j, 1, n)))

    # E(X^2) = k E(X) 를 만족하는 자연수 n
    roots = [sp.nsimplify(s) for s in sp.solve(sp.Eq(EX2, sp.nsimplify(prm['k'])*EX), n)]
    cands = [s for s in roots if s.is_real and s.is_integer and s > 0]
    if not cands:
        raise ValueError(f"k={prm['k']} 에 대응하는 자연수 n 이 없다 (해: {roots})")
    n0 = cands[0]

    # 기댓값의 선형성: E(pX+q) = p E(X) + q
    return sp.nsimplify(sp.simplify(sp.nsimplify(prm['p'])*EX.subs(n, n0) + sp.nsimplify(prm['q'])))


def statement(prm):
    q = sp.nsimplify(prm['q'])
    qs = sp.latex(q) if q.q != 1 else str(q)
    return ("주머니에 1부터 2n+1 까지의 자연수가 하나씩 적힌 2n+1 개의 공이 들어 있다. "
            "임의로 2개를 동시에 꺼내 두 수가 홀수와 짝수이면 그중 짝수를, 모두 홀수이거나 "
            "모두 짝수이면 0 을 기록한다. 기록한 수를 확률변수 X 라 할 때 "
            f"E(X^2)={prm['k']}E(X) 이다. E({prm['p']}X+{qs}) 의 값을 구하시오. (단, n은 자연수이다.)")


print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
