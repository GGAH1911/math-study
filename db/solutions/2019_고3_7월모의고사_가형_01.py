import sympy as sp

# 원문제: 두 벡터 a=(3,-2), b=(2,-6)에 대하여 벡터 a-b의 모든 성분의 합은?
CANDIDATE = 5  # ★원문제 정답 — 절대 바꾸지 않는다

# 수학 구조: a=(a1,a2), b=(b1,b2) 두 평면벡터의 성분 4개가 문제를 결정한다.
# 답 = (a1-b1) + (a2-b2) = (a1+a2) - (b1+b2)  → a1,a2,b1,b2 모두 답을 직접 바꾸는 살아있는 파라미터.
PARAMS = dict(a1=3, a2=-2, b1=2, b2=-6)


def solve(prm):
    """벡터 a-b 의 모든 성분의 합을 sympy 로 실제 계산한다."""
    a1, a2, b1, b2 = (sp.Integer(prm['a1']), sp.Integer(prm['a2']),
                       sp.Integer(prm['b1']), sp.Integer(prm['b2']))
    a = sp.Matrix([a1, a2])
    b = sp.Matrix([b1, b2])
    diff = a - b
    return sp.nsimplify(diff[0] + diff[1])


def statement(prm):
    a1, a2, b1, b2 = prm['a1'], prm['a2'], prm['b1'], prm['b2']
    return (
        f"두 벡터 \\vec{{a}}=({a1}, {a2}), \\vec{{b}}=({b1}, {b2})에 대하여\n"
        f"  벡터 \\vec{{a}}-\\vec{{b}}의 모든 성분의 합은?"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
