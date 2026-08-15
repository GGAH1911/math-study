import sympy as sp

# ─────────────────────────────────────────────────────────────
# 문제 구조
#   X ~ N(m, sigma^2),  f(t) = P(t <= X <= t+w)
#   f(t)는 구간 [t, t+w]의 중점 t+w/2 가 평균 m 과 같을 때 최대가 된다.
#     -> t0 (최댓값을 갖는 t) 이 주어지면  m = t0 + w/2
#   f(m) = P(0 <= Z <= w/sigma) 가 표준정규분포표의 특정 z_key 행 확률과 같다
#     -> sigma = w / z_key
#   구하는 값은 f(query_t) = P(query_t <= X <= query_t+w)
#     -> 표준화하면 z_low=(query_t-m)/sigma, z_high=(query_t+w-m)/sigma = z_low+z_key
#   보기(①~⑤)는 표의 인접한 두 행을 잘못 골랐을 때 나오는 값들
#     (표는 z_low 에서 시작해 step 간격으로 4행: z_low, z_low+step, z_low+2step, z_low+3step)
# ─────────────────────────────────────────────────────────────

CANDIDATE = 1               # ★원문제 정답 보기 번호 (절대 변경 금지)

PARAMS = dict(
    t0=sp.Integer(4),       # f(t)가 최댓값을 갖는 지점 (t=4)
    w=sp.Integer(2),        # 구간 폭: f(t)=P(t<=X<=t+w)  (원문제 w=2)
    z_key=sp.Rational(1),   # f(m)=P(0<=Z<=z_key) 가 표에서 대응하는 z값 → sigma=w/z_key 결정 (원문제 z_key=1.0)
    query_t=sp.Integer(7),  # f(query_t) 를 구하라는 문제 (원문제 query_t=7)
    step=sp.Rational(1, 2), # 표준정규분포표의 z 간격 (원문제 표: 1.0,1.5,2.0,2.5 → step=0.5)
)


def _Phi(z):
    """표준정규분포 누적분포함수 P(Z<=z). erf 를 이용해 sympy 로 실제 계산한다."""
    z = sp.nsimplify(z)
    return sp.Rational(1, 2) * (1 + sp.erf(z / sp.sqrt(2)))


def _geometry(prm):
    t0 = sp.nsimplify(prm['t0'])
    w = sp.nsimplify(prm['w'])
    z_key = sp.nsimplify(prm['z_key'])
    query_t = sp.nsimplify(prm['query_t'])
    if w == 0 or z_key == 0:
        raise ValueError('w, z_key 는 0이 될 수 없다 (구간폭·표준편차 정의 불가)')
    m = t0 + w / 2                 # 최댓값 조건에서 얻는 평균
    sigma = w / z_key               # f(m)=표값 조건에서 얻는 표준편차
    if sigma <= 0:
        raise ValueError('sigma 는 양수여야 한다')
    z_low = (query_t - m) / sigma
    z_high = z_low + z_key          # = (query_t + w - m)/sigma
    return z_low, z_high


def value(prm):
    """f(query_t) 의 실제 값 (소수 넷째 자리, 표준정규분포표 관례에 맞춰 반올림)."""
    z_low, z_high = _geometry(prm)
    v = _Phi(z_high) - _Phi(z_low)
    return round(float(v), 4)


def choices(prm):
    """보기 ①~⑤ 를 표준정규분포표 구조로부터 유도한다.

    표는 z_key 행부터 step 간격으로 4행이 실려 있다고 보고(원문제 표: z=1.0,1.5,2.0,2.5
    → 0.3413,0.4332,0.4772,0.4938), 정답은 2행 떨어진 두 행의 차, 오답은 인접한 행을
    잘못 짝지었을 때 나오는 값들이다. z_key·step 은 sigma 결정과는 별개로 '표 자체의
    모양'을 결정하는 파라미터라, t0·w·query_t 를 바꾸면 실제 값 value(prm) 은 바뀌지만
    보기 목록은 그대로라서 정답 번호가 달라진다.
    """
    z_key = sp.nsimplify(prm['z_key'])
    step = sp.nsimplify(prm['step'])
    if step == 0:
        raise ValueError('표의 z 간격이 0 — 유효한 문제가 아니다')
    Z = [z_key + k * step for k in range(4)]
    P = [round(float(_Phi(z) - _Phi(0)), 4) for z in Z]
    opts = [P[2] - P[0], P[1] - P[0], P[3] - P[1], P[2] - P[1], P[3] - P[2]]
    return [round(o, 4) for o in opts]


def solve(prm):
    """value(prm) 과 가장 가까운 보기의 번호(1~5)를 반환한다."""
    v = value(prm)
    opts = choices(prm)
    idx = min(range(len(opts)), key=lambda i: abs(opts[i] - v))
    return idx + 1


def statement(prm):
    t0 = prm['t0']
    w = prm['w']
    query_t = prm['query_t']
    return (
        f"확률변수 X가 평균이 m, 표준편차가 σ인 정규분포를 따를 때, "
        f"실수 전체의 집합에서 정의된 함수 f(t)는\n"
        f"  f(t) = P(t ≤ X ≤ t+{w})\n"
        f"이다. 함수 f(t)는 t = {t0}에서 최댓값을 갖고, f(m) = 0.3413이다. "
        f"표준정규분포표를 이용하여 f({query_t})의 값을 구한 것은?"
    )


# 원문제 보기와 일치하는지 고정 (base 파라미터 기준)
assert choices(PARAMS) == [0.1359, 0.0919, 0.0606, 0.044, 0.0166], choices(PARAMS)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
