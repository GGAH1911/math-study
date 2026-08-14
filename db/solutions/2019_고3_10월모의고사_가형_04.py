"""
[수능형 문제] 두 사건 A, B가 서로 독립이고
  P(A|B) = p_cond,  P(A∩B^C) = q_inter
일 때 P(B)의 값은? (5지선다)

★수학 구조
  1) A, B가 독립이면 P(A|B) = P(A) 이므로  P(A) = p_cond.
  2) A, B가 독립이면 A, B^C도 독립이므로
       P(A∩B^C) = P(A)·P(B^C) = q_inter
     → P(A)·(1-P(B)) = q_inter  (sympy로 연립방정식을 실제로 풂)
  3) 위 두 식을 풀면 P(B) = 1 - q_inter/p_cond.

★보기(선택지) 구조
  원문제의 보기 5/12, 1/2, 7/12, 2/3, 3/4 는 공차 step=1/12 인 등차수열이고
  정답 3/4 는 그 중 다섯 번째(rank=5, 즉 가장 큰 값)이다.
  이를 일반화해 "공차 step"과 "정답이 몇 번째 보기인가(rank)"를 파라미터로 뽑는다.
  → step, rank 를 바꾸면 같은 확률 값이라도 '몇 번' 보기가 정답인지가 달라진다.
  → p_cond, q_inter 를 바꾸면 P(B) 자체의 값(따라서 보기 전체)이 달라진다.
  네 파라미터가 서로 묶여 있어(보기 구성이 성립하려면 rank가 1~5 범위 안에 있어야 함)
  개별적으로 +1 씩 흔드는 자동검사 대신 VARIANTS 로 성립하는 조합을 직접 제시한다.
"""
from sympy import symbols, Eq, solve as sp_solve, Rational, simplify, nsimplify

CANDIDATE = 5  # ★원문제 정답(보기 번호). 절대 바꾸지 않는다.

# 문제를 정하는 값들
#   p_cond  : P(A|B) (=P(A), 독립이므로)
#   q_inter : P(A∩B^C)
#   step    : 보기(선택지)들의 공차
#   rank    : 정답이 5개 보기 중 몇 번째(1~5)에 오는지
PARAMS = dict(
    p_cond=Rational(1, 3),
    q_inter=Rational(1, 12),
    step=Rational(1, 12),
    rank=5,
)


def value(prm):
    """조건을 연립방정식으로 세워 sympy 로 실제로 풀어 P(B) 를 구한다."""
    pA, pB = symbols('pA pB', positive=True)
    p_cond, q_inter = prm['p_cond'], prm['q_inter']

    eq1 = Eq(pA, p_cond)              # 독립 ⇒ P(A|B)=P(A)
    eq2 = Eq(pA * (1 - pB), q_inter)  # 독립 ⇒ P(A∩B^C)=P(A)P(B^C)

    sols = sp_solve([eq1, eq2], [pA, pB], dict=True)
    if not sols:
        raise ValueError('조건을 만족하는 확률이 없음')
    sol = sols[0]
    pA_val, pB_val = sol[pA], sol[pB]

    if not (0 < pA_val < 1) or not (0 <= pB_val <= 1):
        raise ValueError('확률 값이 [0,1] 범위를 벗어남 — 문제로 성립하지 않음')
    return pB_val


def choices(prm):
    """정답 value 를 rank 번째에 두고 공차 step 인 등차수열 5개를 만든다(값에서 유도)."""
    v = value(prm)
    step, rank = prm['step'], prm['rank']
    if not (1 <= rank <= 5):
        raise ValueError('rank 는 1~5 범위여야 함')
    n_below = rank - 1
    ch = tuple(v - (n_below - i) * step for i in range(5))
    if len(set(simplify(c) for c in ch)) != 5:
        raise ValueError('보기 값이 겹침 — 문제로 성립하지 않음')
    return ch


def solve(prm):
    """value(prm) 이 choices(prm) 중 몇 번째인지(보기 번호, 1~5)를 반환한다."""
    v = value(prm)
    ch = choices(prm)
    for i, c in enumerate(ch, 1):
        if simplify(c - v) == 0:
            return i
    raise ValueError('정답이 보기 목록에 없음')


def statement(prm):
    p_cond, q_inter = prm['p_cond'], prm['q_inter']
    ch = choices(prm)
    marks = ['①', '②', '③', '④', '⑤']
    opts = '  '.join(f'{m} {c}' for m, c in zip(marks, ch))
    return (
        f"두 사건 A와 B가 서로 독립이고\n"
        f"  P(A|B)={p_cond}, P(A∩B^C)={q_inter}\n"
        f"일 때, P(B)의 값은? (단, B^C은 B의 여사건이다.)\n"
        f"{opts}"
    )


# 원문제의 보기와 정확히 일치하는지 고정
assert choices(PARAMS) == (
    Rational(5, 12), Rational(1, 2), Rational(7, 12), Rational(2, 3), Rational(3, 4)
), '유도된 보기가 원문제 보기와 다름'

# rank·step·p_cond·q_inter 가 묶여 있어(성립하는 조합만 유효) VARIANTS 로 실제로 답이
# 달라지는 조합을 제시한다.
VARIANTS = [
    # rank 만 바꿔 정답(보기 번호)이 5 → 1 로 이동
    dict(p_cond=Rational(1, 3), q_inter=Rational(1, 12), step=Rational(1, 12), rank=1),
    # p_cond, q_inter, step, rank 를 모두 바꿔 P(B) 값과 보기 번호가 모두 달라짐
    dict(p_cond=Rational(1, 2), q_inter=Rational(1, 6), step=Rational(1, 6), rank=3),
    # 또 다른 조건값 조합 (P(B)=1/2, 정답은 다섯 번째)
    dict(p_cond=Rational(1, 4), q_inter=Rational(1, 8), step=Rational(1, 8), rank=5),
]

if __name__ == '__main__':
    print('P(B) =', value(PARAMS))
    print('보기 =', choices(PARAMS))
    print('정답 번호 =', solve(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
