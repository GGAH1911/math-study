import sympy as sp
from sympy import sqrt, limit, oo, symbols, floor, Rational

# ------------------------------------------------------------------
# 문제 구조
#   두 곡선 y = sqrt(p*x+q), y = sqrt(r*x+s) 와 직선 x=n 의 교점을
#   A_n=(n, sqrt(p n+q)), B_n=(n, sqrt(r n+s)) 라 하면
#     a_n = OA_n = sqrt(n^2+p n+q),  b_n = OB_n = sqrt(n^2+r n+s)
#   lim_{n->oo} C/(a_n-b_n) 를 구하는 문제.
#
#   a_n^2-b_n^2 = (p-r)n+(q-s) 이고 a_n+b_n ~ 2n 이므로
#     lim (a_n-b_n) = (p-r)/2   (q,s 는 유리화 후 n->oo 극한에서 소거되어
#                                 정답 자체에는 영향을 주지 않는, 곡선의
#                                 절편을 정하는 순수한 배경 파라미터다)
#   따라서 value = 2C/(p-r).
#
#   p, r, C 를 바꾸면 값이 실제로 바뀐다(라이브 파라미터). q, s 는 그래프의
#   x절편(그림에 -4/5, 1/2 로 표시)만 바꿀 뿐 극한값에는 영향이 없다.
# ------------------------------------------------------------------

CANDIDATE = 3   # ★원문제 정답(보기 번호) — 절대 바꾸지 않음

PARAMS = dict(
    p=5,   # 위쪽 곡선 y=sqrt(p x+q) 의 x계수
    q=4,   # 위쪽 곡선의 상수항 (x절편 -q/p = -4/5)
    r=2,   # 아래쪽 곡선 y=sqrt(r x+s) 의 x계수
    s=-1,  # 아래쪽 곡선의 상수항 (x절편 -s/r = 1/2)
    C=12,  # 극한식 분자의 상수
)

# 보기 5개를 만들 때 쓰는 '창(window)' 상수. D=보기 간격, K=원문제가 보기 중
# 정확히 3번째(가운데)에 오도록 맞춘 고정 오프셋. 문제 그 자체의 수학과는
# 무관한 순수 표시(디자인) 상수이므로 PARAMS 에 넣지 않는다.
D = 2
K = 2


def value(prm):
    """lim_{n->oo} C/(a_n-b_n) 을 sympy 로 직접 계산한다."""
    p, q, r, s, C = prm['p'], prm['q'], prm['r'], prm['s'], prm['C']
    if p == r:
        raise ValueError('p==r 이면 a_n-b_n 이 n에 무관한 극한을 갖지 않는다(문제 성립 안 함)')
    n = symbols('n', positive=True)
    a_n = sqrt(n**2 + p*n + q)
    b_n = sqrt(n**2 + r*n + s)
    val = limit(C / (a_n - b_n), n, oo)
    if not val.is_number or val.has(sp.zoo, sp.nan, sp.oo, -sp.oo):
        raise ValueError(f'유효한 극한값이 아니다: {val}')
    return sp.nsimplify(val)


def choices(prm):
    """정답 값 주위로 등간격(D) 5지선다 보기를 만든다.

    idx0 = floor(value/D) 를 5로 나눈 나머지(고정 오프셋 K 적용)로 정답의
    '창' 위치를 잡으므로, value 가 바뀌면 5지선다 중 정답의 순번도 실제로
    바뀐다(파라미터가 답 자체 뿐 아니라 보기 번호까지 흔든다).
    """
    val = value(prm)
    idx0 = floor(val / D)
    j = int(idx0 - K) % 5
    window_start = idx0 - j
    return [int((window_start + i) * D) for i in range(5)]


def solve(prm):
    """5지선다 보기 번호(1~5)를 돌려준다."""
    val = value(prm)
    idx0 = floor(val / D)
    j = int(idx0 - K) % 5
    return j + 1


def statement(prm):
    p, q, r, s, C = prm['p'], prm['q'], prm['r'], prm['s'], prm['C']

    def lin(coef, const):
        t = f"{coef}x"
        if const > 0:
            t += f"+{const}"
        elif const < 0:
            t += f"{const}"
        return t

    ch = choices(prm)
    opts = ['①', '②', '③', '④', '⑤']
    opt_str = '  '.join(f'{o} {v}' for o, v in zip(opts, ch))
    return (
        f"자연수 n에 대하여 직선 x=n이 두 곡선 y=√({lin(p, q)}), y=√({lin(r, s)})와 "
        f"만나는 점을 각각 A_n, B_n이라 하자. 선분 OA_n의 길이를 a_n, 선분 OB_n의 길이를 "
        f"b_n이라 할 때, lim_{{n→∞}} {C}/(a_n-b_n)의 값은? (단, O는 원점이다.)\n"
        f"{opt_str}"
    )


# 원문제 보기가 정확히 재현되는지 고정
assert choices(PARAMS) == [4, 6, 8, 10, 12]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
