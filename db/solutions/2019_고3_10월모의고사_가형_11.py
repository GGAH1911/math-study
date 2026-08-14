# [원문제] 포물선 y^2=4px 위의 점 P를 지나고 y축에 수직인 직선이 포물선 y^2=-4px와
#   만나는 점을 Q라 하자. OP=PF (F는 초점) 이고 PQ=6일 때, 선분 PF의 길이는?
#
# [수학 구조]
#   P=(x1,y1)를 y1^2=4p x1 로 두면, Q는 y좌표가 같고 y^2=-4px 위에 있으므로
#   Q=(-x1,y1) — 즉 원점에 대해 P와 x축방향으로 대칭이다. 따라서 PQ=2x1 이고
#   x1 = PQ/2 가 즉시 정해진다(선분 길이 L이 x1 을 결정하는 첫 번째 손잡이).
#
#   초점 F=(p,0). 조건 OP=PF, 즉 OP^2=PF^2 을 sympy 로 실제로 풀어 p를 구하고
#   PF = sqrt((x1-p)^2 + 4p*x1) 를 계산한다 — 원문제 수치(x1=3)를 하드코딩하지 않고
#   L(=PQ)에서 유도한다.
#
#   보기(①~⑤)는 원문제에서 7,8,9,10,11 로 등차수열(첫 보기 choice_base, 공차
#   choice_step)이다. choices()는 이 두 입력에서 등차수열로 유도하고, solve()는
#   실제로 계산한 PF 값이 그 수열의 몇 번째 항인지 찾는다(안 맞으면 예외).
#
#   L, choice_base, choice_step 세 파라미터 중 실제로 답(보기 번호)을 바꾸는 것을
#   직접 solve() 를 돌려 확인함: choice_base, choice_step 은 각각 단독으로 바꿔도
#   보기 번호가 바뀐다(L 은 7~11 사이에서 PF가 정확히 정수로 떨어지는 값이 L=6 하나뿐이라
#   기본 보기 범위 안에서는 단독으로 못 움직이지만, 보기 범위를 함께 넓히면 L도 움직인다
#   — 아래 VARIANTS 참고).

import sympy as sp

CANDIDATE = 3  # 원문제 정답: ③ 9   (절대 변경 금지)

PARAMS = dict(
    L=6,             # 선분 PQ의 길이
    choice_base=7,   # 보기 ①의 값
    choice_step=1,   # 보기 사이의 공차
)

# L(=PQ)은 기본 보기 범위(7~11, 폭이 좁음)에서는 단독 섭동으로 못 움직이므로,
# 보기 범위를 함께 넓힌 성립 조합을 직접 제시해 L도 진짜 손잡이임을 보인다.
VARIANTS = [
    PARAMS,
    dict(choice_base=8, choice_step=1),                 # 값(9)은 그대로, 보기만 이동 -> ②
    dict(choice_base=7, choice_step=2),                 # 공차만 바뀜 -> ②
    dict(L=8, choice_base=10, choice_step=1),            # L을 바꿔 값 자체가 12로 이동 -> ③
    dict(L=10, choice_base=13, choice_step=1),           # L을 더 바꿔 값이 15로 이동 -> ③
]


def value(prm):
    """PQ=L, OP=PF 조건으로부터 PF의 길이를 sympy로 실제로 푼다."""
    L = sp.nsimplify(prm['L'])
    if L <= 0:
        raise ValueError('PQ 길이 L 은 양수여야 한다')
    x1 = L / 2

    p = sp.symbols('p', positive=True)
    y1_sq = 4 * p * x1                       # y1^2 = 4p*x1  (점 P가 포물선 위에 있다는 조건)
    OP_sq = x1 ** 2 + y1_sq
    PF_sq = (x1 - p) ** 2 + y1_sq            # F = (p, 0)

    sols = [s for s in sp.solve(sp.Eq(OP_sq, PF_sq), p) if s.is_real and s > 0]
    if not sols:
        raise ValueError('OP=PF 를 만족하는 양수 p 가 존재하지 않는다')
    p_val = sols[0]

    PF = sp.sqrt((x1 - p_val) ** 2 + 4 * p_val * x1)
    return sp.nsimplify(sp.simplify(PF))


def choices(prm):
    """입력 choice_base/choice_step 에서 유도한 5개의 보기(등차수열)."""
    base = sp.nsimplify(prm['choice_base'])
    step = sp.nsimplify(prm['choice_step'])
    if step == 0:
        raise ValueError('보기 공차 choice_step 은 0 일 수 없다')
    return [base + step * i for i in range(5)]


def solve(prm):
    """정답 보기 번호(1~5)."""
    v = value(prm)
    opts = choices(prm)
    if v not in opts:
        raise ValueError(f'PF={v} 가 보기 {opts} 중 어디에도 해당하지 않는다')
    return opts.index(v) + 1


def statement(prm):
    L = prm['L']
    opts = choices(prm)
    circles = ['①', '②', '③', '④', '⑤']
    opt_str = ' '.join(f'{circles[i]} {c}' for i, c in enumerate(opts))
    return (
        f"그림과 같이 점 F가 초점인 포물선 y^2=4px 위의 점 P를 지나고 y축에 수직인 직선이 "
        f"포물선 y^2=-4px와 만나는 점을 Q라 하자. OP=PF이고 PQ={L}일 때, 선분 PF의 길이는? "
        f"(단, O는 원점이고, p는 양수이다.)\n{opt_str}"
    )


# 원문제 보기(7,8,9,10,11) 재현 확인
assert choices(PARAMS) == [7, 8, 9, 10, 11]
assert value(PARAMS) == 9

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
