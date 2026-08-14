"""2026 고3 7월 모의고사 공통 3번 — 시그마의 선형성 (파라미터화 솔버)

유형: sum_{k=1}^{n}(ck*k + ca*a_k) = total 일 때 sum_{k=1}^{n} a_k 의 값은?
구조: 시그마의 선형성으로 sum(ck*k) 를 분리 → ca * S = total - sum(ck*k) → S.
      객관식이므로 계산된 S 를 보기 목록과 대조해 보기 번호를 답으로 돌려준다.
"""
import sympy as sp

CANDIDATE = 1

PARAMS = dict(
    n=5,            # 시그마 범위 k = 1..n
    coef_k=1,       # 괄호 안 k 의 계수
    coef_a=3,       # 괄호 안 a_k 의 계수
    total=27,       # 시그마 전체의 값
    choices=(4, 5, 6, 7, 8),   # ①~⑤ 보기 값 (정답 번호는 solve 가 대조해 정한다)
)


def sigma_sum(prm):
    """조건식을 풀어 sum_{k=1}^{n} a_k 의 값을 구한다."""
    k, S = sp.symbols('k S')
    n = sp.Integer(prm['n'])
    lin = sp.summation(sp.Integer(prm['coef_k']) * k, (k, 1, n))   # sum ck*k = ck*n(n+1)/2
    eq = sp.Eq(lin + sp.Integer(prm['coef_a']) * S, sp.Integer(prm['total']))
    return sp.simplify(sp.solve(eq, S)[0])


def solve(prm):
    """계산한 합을 보기와 대조해 정답 보기 번호(1~5)를 반환. 보기에 없으면 0."""
    val = sigma_sum(prm)
    for i, c in enumerate(prm['choices'], start=1):
        if sp.simplify(val - sp.nsimplify(c)) == 0:
            return i
    return 0


def statement(prm):
    n, ck, ca, total = prm['n'], prm['coef_k'], prm['coef_a'], prm['total']
    kterm = 'k' if ck == 1 else f'{ck}k'
    aterm = 'a_{k}' if ca == 1 else f'{ca}a_{{k}}'
    body = (f"수열 {{a_n}}에 대하여 \\sum_{{k=1}}^{{{n}}}({kterm}+{aterm})={total}일 때, "
            f"\\sum_{{k=1}}^{{{n}}}a_{{k}}의 값은?")
    marks = '①②③④⑤'
    opts = ' '.join(f'{marks[i]} {c}' for i, c in enumerate(prm['choices']))
    return f"{body}\n{opts}"


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
