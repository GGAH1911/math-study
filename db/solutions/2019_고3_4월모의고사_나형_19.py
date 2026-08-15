import sympy as sp

# ── 문제의 수학 구조 ────────────────────────────────────────────────────
# f(x) = 1/(x+1) - a   (수평점근선 y=-a, a 를 바꿔도 f(x)=-a 는 1/(x+1)=0 이 되어
#                        절대 해가 없다 → ㄱ은 항상 참인 구조적 사실)
# g(x) = √(x+1)        (정의역 0≤x≤N, N=M²-1 로 두면 g(N)=M 이 되어 y좌표가
#                        정수인 점이 정확히 M개 생긴다)
# ㄴ, ㄷ 은 "실제 계산값"과 "문제가 주장하는 값(claimed_B, claimed_C)"이 같은지를
# 묻는 명제다 — 주장값을 실제값과 다르게 흔들면 그 보기는 거짓이 되어 정답(보기 번호)이
# 바뀐다. 즉 a·M·claimed_B·claimed_C 네 개가 모두 답을 바꾸는 진짜 손잡이다.

CANDIDATE = 5  # ★원문제 정답: ⑤ ㄱ,ㄴ,ㄷ

PARAMS = dict(
    a=5,          # f(x)=1/(x+1)-a 의 수직이동(=수평점근선 위치)
    M=3,          # 정의역을 [0, M^2-1] 로 만드는 계수 (g(x)의 최댓값이 M)
    claimed_B=3,  # ㄴ이 주장하는 "y좌표가 정수인 점의 개수"
    claimed_C=61, # ㄷ이 주장하는 "정수 격자점의 개수"
)

CHOICE_LABELS = [
    ('ㄱ',),
    ('ㄱ', 'ㄴ'),
    ('ㄱ', 'ㄷ'),
    ('ㄴ', 'ㄷ'),
    ('ㄱ', 'ㄴ', 'ㄷ'),
]


def value(prm):
    """세 명제 ㄱ,ㄴ,ㄷ 각각의 참/거짓을 실제로 sympy 로 계산해 참인 것들의 라벨 튜플을 낸다."""
    a = prm['a']
    M = int(prm['M'])
    claimed_B = prm['claimed_B']
    claimed_C = prm['claimed_C']
    if M < 1:
        raise ValueError('M(정의역 상한을 정하는 계수)은 1 이상의 정수여야 한다')
    N = M * M - 1

    x = sp.symbols('x', real=True)
    f = 1 / (x + 1) - a
    g = sp.sqrt(x + 1)

    # ㄱ: f(x) = -a 를 만족하는 x 가 있는가 (있으면 곡선이 직선 y=-a 와 만난다)
    solA = sp.solve(sp.Eq(f, -a), x)
    A_true = (len(solA) == 0)

    # ㄴ: 0<=x<=N 에서 g(x) 의 y좌표가 정수인 점의 실제 개수
    ys = set()
    for y in range(0, M + 5):
        xv = y * y - 1
        if 0 <= xv <= N:
            ys.add(y)
    B_count = len(ys)
    B_true = (B_count == claimed_B)

    # ㄷ: f(x)<=y<=g(x), 0<=x<=N 영역의 정수 격자점 실제 개수
    total = 0
    for xi in range(0, N + 1):
        fv = sp.Rational(1, xi + 1) - a
        gv = sp.sqrt(sp.Integer(xi + 1))
        lo = sp.ceiling(fv)
        hi = sp.floor(gv)
        total += int(hi - lo + 1)
    C_true = (total == claimed_C)

    return tuple(l for cond, l in zip((A_true, B_true, C_true), ('ㄱ', 'ㄴ', 'ㄷ')) if cond)


def choices(prm):
    # 원문제의 보기 구조(① ㄱ ② ㄱㄴ ③ ㄱㄷ ④ ㄴㄷ ⑤ ㄱㄴㄷ)는 조합 방식 자체이므로 고정.
    return CHOICE_LABELS


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    assert ch == CHOICE_LABELS  # 원문제 보기 구성과 동일한지 고정
    if v not in ch:
        raise ValueError(f'참인 명제 조합 {v} 이 보기 목록에 없다 — 이 파라미터 조합은 문제로 성립하지 않는다')
    return ch.index(v) + 1


def statement(prm):
    a = prm['a']
    M = int(prm['M'])
    N = M * M - 1
    claimed_B = prm['claimed_B']
    claimed_C = prm['claimed_C']
    return (
        f"좌표평면에서 두 함수 f(x)=1/(x+1)-{a}, g(x)=√(x+1)의 그래프에 대하여 "
        f"<보기>에서 옳은 것만을 있는 대로 고른 것은?\n"
        f"<보 기>\n"
        f"ㄱ. 곡선 y=f(x)는 직선 y=-{a}와 만나지 않는다.\n"
        f"ㄴ. 0≤x≤{N}일 때, 곡선 y=g(x) 위에 있는 점 중에서 y좌표가 정수인 점의 개수는 {claimed_B}이다.\n"
        f"ㄷ. 두 곡선 y=f(x), y=g(x)와 두 직선 x=0, x={N}으로 둘러싸인 영역의 내부 또는 그 경계에 "
        f"포함되고 x좌표와 y좌표가 모두 정수인 점의 개수는 {claimed_C}이다.\n"
        f"① ㄱ  ② ㄱ,ㄴ  ③ ㄱ,ㄷ  ④ ㄴ,ㄷ  ⑤ ㄱ,ㄴ,ㄷ"
    )


if __name__ == '__main__':
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
