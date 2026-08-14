# 원점에서 출발해 수직선 위를 움직이는 점 P의 속도 v(t)=a*t^2+b*t+k.
#   ㄱ: k=k1 이면 시각 t=t1 에서 점 P의 위치는 pos1 이다.
#   ㄴ: k=k2 이면 [0,T2] 에서 움직인 거리 = 위치의 변화량 이다.
#   ㄷ: k=k3 이면 [0,T3] 에서 움직인 거리는 dist3 이다.
# 위치 x(t)=∫_0^t v, 움직인 거리 = ∫|v| (속도의 부호가 바뀌는 곳에서 쪼갠다).
import sympy as sp

CANDIDATE = 3

# 문제가 준 수치만 파라미터로 둔다(유도값 아님).
PARAMS = dict(
    a=3, b=-6,          # v(t) = a t^2 + b t + k
    k1=0,  t1=1, pos1=-2,   # ㄱ
    k2=2,  T2=3,            # ㄴ
    k3=-9, T3=4, dist3=34,  # ㄷ
)

# 보기(선택지) — 각 번호가 주장하는 '옳은 것'의 조합. 정답 번호는 solve 가 계산한다.
CHOICES = {1: ('ㄱ',), 2: ('ㄱ', 'ㄴ'), 3: ('ㄱ', 'ㄷ'),
           4: ('ㄴ', 'ㄷ'), 5: ('ㄱ', 'ㄴ', 'ㄷ')}

t = sp.Symbol('t', real=True)


def _v(prm, kv):
    return sp.nsimplify(prm['a']) * t**2 + sp.nsimplify(prm['b']) * t + sp.nsimplify(kv)


def _x(prm, kv, tv):
    """원점 출발이므로 위치 = ∫_0^tv v dt."""
    return sp.integrate(_v(prm, kv), (t, 0, sp.nsimplify(tv)))


def _turns(prm, kv, t0, t1_):
    """구간 내부에서 속도의 부호가 실제로 바뀌는 시각들."""
    out = []
    for r in sp.solve(sp.Eq(_v(prm, kv), 0), t):
        if r.is_real and sp.simplify(r - t0) > 0 and sp.simplify(t1_ - r) > 0:
            out.append(sp.nsimplify(r))
    return sorted(set(out), key=lambda z: float(z))


def _dist(prm, kv, t0, t1_):
    """움직인 거리 = ∫|v| — 방향이 바뀌는 지점에서 끊어 위치 변화량의 절댓값을 더한다."""
    t0, t1_ = sp.nsimplify(t0), sp.nsimplify(t1_)
    edges = [t0] + _turns(prm, kv, t0, t1_) + [t1_]
    total = 0
    for i in range(len(edges) - 1):
        total += sp.Abs(_x(prm, kv, edges[i + 1]) - _x(prm, kv, edges[i]))
    return sp.simplify(total)


def solve(prm):
    """조건 → 정답 보기 번호 (일치하는 보기가 없으면 0)."""
    # ㄱ: 위치 x(t1) 이 pos1 인가
    g = sp.simplify(_x(prm, prm['k1'], prm['t1']) - sp.nsimplify(prm['pos1'])) == 0
    # ㄴ: 움직인 거리와 (부호 있는) 위치의 변화량이 같은가 — 되돌아오면 달라진다
    n = sp.simplify(_dist(prm, prm['k2'], 0, prm['T2'])
                    - _x(prm, prm['k2'], prm['T2'])) == 0
    # ㄷ: 움직인 거리가 dist3 인가
    d = sp.simplify(_dist(prm, prm['k3'], 0, prm['T3']) - sp.nsimplify(prm['dist3'])) == 0

    truth = tuple(nm for nm, ok in zip(('ㄱ', 'ㄴ', 'ㄷ'), (g, n, d)) if bool(ok))
    for num, combo in CHOICES.items():
        if tuple(combo) == truth:
            return num
    return 0


def statement(prm):
    """파라미터로부터 새 문제 문장을 만든다."""
    def sgn(c, sym):
        c = sp.nsimplify(c)
        if c == 0:
            return ''
        return f" {'+' if c > 0 else '-'} {sp.Abs(c)}{sym}"
    lead = '' if sp.nsimplify(prm['a']) == 1 else f"{sp.nsimplify(prm['a'])}"
    body = f"{lead}t^2{sgn(prm['b'], 't')} + k"
    return (
        "시각 t=0일 때 원점을 출발하여 수직선 위를 움직이는 점 P가 있다. "
        f"실수 k에 대하여 시각 t(t≥0)일 때 점 P의 속도가 v(t)={body} 이다. "
        "<보기>에서 옳은 것만을 있는 대로 고른 것은?\n"
        f"ㄱ. k={prm['k1']}이면, 시각 t={prm['t1']}일 때 점 P의 위치는 {prm['pos1']}이다.\n"
        f"ㄴ. k={prm['k2']}이면, 시각 t=0에서 t={prm['T2']}까지 점 P가 움직인 거리는 "
        "점 P의 위치의 변화량과 같다.\n"
        f"ㄷ. k={prm['k3']}이면, 시각 t=0에서 t={prm['T3']}까지 점 P가 움직인 거리는 {prm['dist3']}이다.\n"
        "① ㄱ ② ㄱ,ㄴ ③ ㄱ,ㄷ ④ ㄴ,ㄷ ⑤ ㄱ,ㄴ,ㄷ"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
