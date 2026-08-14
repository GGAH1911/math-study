# 1..2n+1 이 적힌 공에서 2개를 꺼내, 홀·짝 하나씩이면 그 짝수를, 아니면 0 을 기록 → X.
# E(X^2)=k·E(X) 조건으로 n 을 정하고 E(pX+q) 를 구한다.
#
# ★파라미터화 솔버(scripts/CLAUDE.md 규격): PARAMS 를 바꾸면 같은 유형의 새 문제와
#   검증된 답이 그대로 나온다. 원문제는 PARAMS 기본값으로 재현된다.
CANDIDATE = 41
import sympy as sp

PARAMS = dict(k=14, p=7, q=sp.Rational(2, 3))     # E(X^2)=k E(X), 구하는 값 E(pX+q)


def solve(prm):
    n = sp.symbols('n', positive=True, integer=True)
    tot = sp.binomial(2*n + 1, 2)                  # 두 공을 뽑는 경우의 수
    w = (n + 1)/tot                                # 짝수 하나(2k) + 홀수 하나 → 확률
    j = sp.symbols('j', positive=True, integer=True)
    EX = sp.simplify(sp.summation(2*j*w, (j, 1, n)))
    EX2 = sp.simplify(sp.summation((2*j)**2*w, (j, 1, n)))
    n0 = [s for s in sp.solve(sp.Eq(EX2, prm['k']*EX), n) if s.is_real and s > 0][0]
    return sp.nsimplify(sp.simplify(prm['p']*EX.subs(n, n0) + prm['q']))


def statement(prm):
    return (f"1부터 2n+1 까지 적힌 공에서 2개를 꺼내 홀·짝이면 그 짝수를, 아니면 0 을 기록한 값을 X 라 하자. "
            f"E(X^2)={prm['k']}E(X) 일 때 E({prm['p']}X+{prm['q']}) 의 값은?")


print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
