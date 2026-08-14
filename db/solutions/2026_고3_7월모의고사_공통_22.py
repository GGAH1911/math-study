# 곡선1 y = base^(x-m) + n 위의 A(a,b) (a<b, 제1사분면), B 는 A 를 y=x 에 대칭시킨 점 (b,a).
# 곡선2 y = log_base(x - n + sx) + m - sy  (= 곡선1의 역함수를 sx 만큼 왼쪽·sy 만큼 아래로 평행이동).
# B 중심 반지름 √R2 인 원이 곡선2 와 만나는 두 점 중 x 가 작은 점이 C.
# (가) AC ⊥ (y = ps·x) → 직선 AC 의 기울기 s = -1/ps.
# (나) [AOB]:[ACB] = r.
#
# ── 구조(파라미터로 재유도) ───────────────────────────────────────────────────
# p = a - m, u = log_base(c - n + sx) 로 두면
#   A = (m+p, n+base^p),  B = (n+base^p, m+p),  C = (n-sx+base^u, m-sy+u)
#   C - B = (base^u - base^p - sx, u - p - sy)  →  m,n 이 소거된다.
# 따라서 원 조건은 t := u-p 에 대한 식  (base^p(base^t - 1) - sx)^2 + (t-sy)^2 = R2 뿐이고,
# (t-sy)^2 ≤ R2 이므로 t 는 [sy-√R2, sy+√R2] 안에서만 찾으면 된다(유한 구간 전수 스캔).
# 원문제는 sx^2+sy^2 = R2 라서 t=0(=C 가 B 에서 (-sx,-sy) 만큼 떨어진 점)이 항상 근이고
# 그것이 x 가 가장 작은 교점이다 — 이 특수성 덕분에 A 가 곡선 위를 움직여도 조건이 유지된다.
# 남은 두 조건 (가)(나)는 d = n-m 과 S = m+n 을 p 의 함수로 확정시킨다:
#   (가) d(1+s) = u - sy - base^p + s·sx - s·base^u + s·p
#   (나) a+b = r·|s+1|·|c-a|      → S = r|s+1||c-a| - p - base^p
# 그러면 m(p) = (S-d)/2, n(p) = (S+d)/2 이고, m·n 이 **동시에 자연수**가 되는 p 만 답이 된다.
# S = m+n 은 p 에 대해 감소하므로 가장 작은 유효 p 가 최댓값을 준다.
CANDIDATE = 26
import math
import sympy as sp

# 문제가 준 수치
#
# ★반지름은 **자유 파라미터가 아니다**(2026-08-14 수정). 위 주석의 t=0 특수성이 바로
#   R² = sx² + sy² 일 때만 성립한다: φ(0) = (-sx)² + (0-sy)² - R² = sx²+sy²-R².
#   예전엔 radius_sq 를 따로 뒀는데, 그러면 sx 나 sy 만 흔드는 순간 설계가 깨져
#   교점이 사라지고 solve 가 **조용히 None** 을 돌려줬다(장식 파라미터로 보인 원인).
#   유도값으로 묶으니 sx·sy 가 진짜 손잡이가 된다.
PARAMS = dict(
    base=2,                          # 두 곡선의 밑 (y=2^(x-m)+n, y=log_2(...))
    log_shift_x=1,                   # 곡선2 의 x - n + 1 에서 +1
    log_shift_y=7,                   # 곡선2 의 + m - 7 에서 7
    perp_slope=sp.Rational(1, 3),    # (가) AC 와 수직인 직선 y = (1/3)x 의 기울기
    area_ratio=sp.Rational(27, 8),   # (나) [AOB] : [ACB] = 27 : 8
)


# ★파라미터가 서로 묶여 있다. m, n 이 **동시에 자연수**여야 하므로 sx 하나만 1→2 로
#   바꾸면 해가 사라진다 — 조합으로 움직여야 한다(sx·sy 를 함께 2배 하면 성립).
#   그래서 성립하는 조합을 직접 제시한다. 게이트가 이걸 돌려 재생성 능력을 확인한다.
#   (아래는 전수 탐색으로 찾은 94개 유효 조합 중 답이 서로 다른 대표 5개)
VARIANTS = [
    dict(log_shift_x=2, log_shift_y=14),                              # → 53 (원문제의 2배 스케일)
    dict(area_ratio=sp.Rational(15, 8)),                              # → 14 (넓이비만)
    dict(log_shift_x=2, log_shift_y=6, area_ratio=sp.Rational(4)),    # → 31
    dict(log_shift_x=1, log_shift_y=3, area_ratio=sp.Rational(9, 4)),  # → 8
    dict(log_shift_x=1, log_shift_y=3, area_ratio=sp.Rational(5, 2),
         perp_slope=sp.Rational(1, 5)),                               # → 9 (기울기까지)
]


def radius_sq(prm):
    """원의 반지름의 제곱 — 설계 불변식 R² = sx² + sy².
    이 값이라야 A 가 곡선 위 어디에 있든 원이 곡선2 와 만나는 점이 존재한다."""
    return sp.Integer(prm['log_shift_x'])**2 + sp.Integer(prm['log_shift_y'])**2

# 탐색창(문제 수치가 아니라 계산 설정) — a-m 의 탐색 범위와 격자
P_LO, P_HI, P_N = -8.0, 12.0, 800
T_N = 700
TOL = 1e-7


def _consts(prm):
    """PARAMS → 계산에 쓰는 실수 상수. s 는 (가)로부터 얻는 직선 AC 의 기울기."""
    base = float(prm['base'])
    sx = float(prm['log_shift_x'])
    sy = float(prm['log_shift_y'])
    r2 = float(radius_sq(prm))         # ★유도값 — 자유 파라미터가 아니다
    ps = float(prm['perp_slope'])
    r = float(prm['area_ratio'])
    if base <= 1 or r2 <= 0 or ps == 0:
        raise ValueError('불가능한 파라미터')
    s = -1.0 / ps                      # 수직 조건
    if abs(1.0 + s) < 1e-12:           # AB(기울기 -1)와 평행 → 삼각형 ACB 가 뭉개진다
        raise ValueError('AC 가 AB 와 평행')
    return base, sx, sy, r2, s, r


def _phi(t, K, base, sx, sy, r2):
    """|BC|^2 - R^2 을 t = u - p 의 함수로. (K = base^p)"""
    return (K * (base ** t - 1.0) - sx) ** 2 + (t - sy) ** 2 - r2


def _t_roots(K, base, sx, sy, r2):
    """원과 곡선2 의 교점 전부를 t 로. (t-sy)^2 ≤ R2 라 구간이 유한하다."""
    rad = math.sqrt(r2)
    lo, hi = sy - rad, sy + rad
    h = (hi - lo) / T_N
    out = []
    pt, pv = lo, _phi(lo, K, base, sx, sy, r2)
    for i in range(1, T_N + 1):
        t = lo + i * h
        v = _phi(t, K, base, sx, sy, r2)
        if pv == 0.0:
            out.append(pt)
        elif pv * v < 0.0:
            a, b, fa = pt, t, pv
            for _ in range(80):
                mid = 0.5 * (a + b)
                fm = _phi(mid, K, base, sx, sy, r2)
                if fm == 0.0:
                    a = b = mid
                    break
                if fa * fm < 0.0:
                    b = mid
                else:
                    a, fa = mid, fm
            out.append(0.5 * (a + b))
        pt, pv = t, v
    if pv == 0.0:
        out.append(pt)
    return out


def _mn(p, base, sx, sy, r2, s, r):
    """A 의 위치(p = a-m)를 주면 (가)(나)가 요구하는 m, n 을 돌려준다."""
    try:
        K = base ** p
        roots = _t_roots(K, base, sx, sy, r2)
        if len(roots) < 2:              # 원이 곡선2 와 두 점에서 만나야 한다
            return None
        u = p + roots[0]                # x 좌표가 가장 작은 교점이 C
        bu = base ** u
        d = (u - sy - K + s * sx - s * bu + s * p) / (1.0 + s)      # (가)
        ca = d - sx + bu - p                                        # c - a
        big = r * abs(s + 1.0) * abs(ca) - p - K                    # (나) → S = m+n
        return (big - d) / 2.0, (big + d) / 2.0
    except (OverflowError, ValueError, ZeroDivisionError):
        return None


def _valid(m, n, p, base, sx, sy, r2, s, r):
    """정수쌍 (m,n) 이 실제로 문제의 모든 조건을 만족하는지 원식으로 되짚는다."""
    if m < 1 or n < 1:
        return False
    a, b = m + p, n + base ** p
    if a <= 0 or b <= 0 or not a < b:            # 제1사분면 + a<b
        return False
    K = base ** p
    roots = _t_roots(K, base, sx, sy, r2)
    if len(roots) < 2:
        return False
    u = p + roots[0]
    c, yc = n - sx + base ** u, m - sy + u
    if c - n + sx <= 0:                           # 로그 정의역
        return False
    if abs((c - b) ** 2 + (yc - a) ** 2 - r2) > 1e-6 * max(1.0, r2):
        return False
    if abs((yc - b) - s * (c - a)) > 1e-6 * max(1.0, abs(c - a)):   # (가)
        return False
    aob = 0.5 * abs(a - b) * abs(a + b)
    acb = 0.5 * abs(b - a) * abs(c - a) * abs(s + 1.0)
    if acb <= 1e-12:
        return False
    return abs(aob / acb - r) < 1e-6 * r


def _p_for_m(pa, pb, tm, cs):
    """구간 [pa,pb] 안에서 m(p) = tm 인 p 를 이분법으로. 없으면 None."""
    va, vb = _mn(pa, *cs), _mn(pb, *cs)
    if va is None or vb is None:
        return None
    fa, fb = va[0] - tm, vb[0] - tm
    if fa == 0.0:
        return pa
    if fb == 0.0:
        return pb
    if fa * fb > 0.0:
        return None
    for _ in range(60):
        pm = 0.5 * (pa + pb)
        if pm == pa or pm == pb:
            break
        vm = _mn(pm, *cs)
        if vm is None:
            return None
        fm = vm[0] - tm
        if fm == 0.0:
            return pm
        if fa * fm < 0.0:
            pb = pm
        else:
            pa, fa = pm, fm
    return 0.5 * (pa + pb)


def solve(prm):
    """조건을 만족시키는 자연수 m, n 을 모두 찾아 m+n 의 최댓값을 돌려준다."""
    cs = _consts(prm)
    grid = [P_LO + i * (P_HI - P_LO) / P_N for i in range(P_N + 1)]
    vals = [_mn(p, *cs) for p in grid]
    best, seen = None, set()
    for i in range(P_N):
        v0, v1 = vals[i], vals[i + 1]
        if v0 is None or v1 is None:
            continue
        m0, m1 = v0[0], v1[0]
        if abs(m1 - m0) > 3.0:                    # 가지가 끊긴 구간은 건너뛴다
            continue
        lo, hi = (m0, m1) if m0 <= m1 else (m1, m0)
        for tm in range(int(math.floor(lo)), int(math.floor(hi)) + 2):
            if not (lo - 1e-12 <= tm <= hi + 1e-12) or tm < 1:
                continue
            root = _p_for_m(grid[i], grid[i + 1], tm, cs)
            if root is None:
                continue
            got = _mn(root, *cs)
            if got is None:
                continue
            mv, nv = got
            m_i, n_i = round(mv), round(nv)
            if abs(mv - m_i) > TOL or abs(nv - n_i) > TOL:
                continue                          # m, n 이 동시에 자연수여야 한다
            if (m_i, n_i) in seen:
                continue
            if not _valid(m_i, n_i, root, *cs):
                continue
            seen.add((m_i, n_i))
            tot = m_i + n_i
            if best is None or tot > best:
                best = tot
    if best is None:
        # ★조용히 None 을 돌려주면 "답이 안 바뀐다"와 구별이 안 된다. 크게 실패시킨다.
        raise ValueError('조건을 만족하는 자연수 (m, n) 이 없다 — 파라미터 조합이 문제로 성립하지 않음')
    return best


def statement(prm):
    """같은 유형의 새 문제 문장."""
    base = prm['base']
    sx, sy = prm['log_shift_x'], prm['log_shift_y']
    rad = sp.nsimplify(sp.sqrt(radius_sq(prm)))
    ps, r = sp.nsimplify(prm['perp_slope']), sp.Rational(prm['area_ratio'])
    return (
        f"두 자연수 m, n 에 대하여 곡선 y={base}^(x-m)+n 위의 점 A(a,b)(a<b)가 제1사분면에 있다. "
        f"점 A 를 직선 y=x 에 대하여 대칭이동한 점을 B 라 하자. "
        f"점 B 를 중심으로 하고 반지름의 길이가 {rad} 인 원이 "
        f"곡선 y=log_{base}(x-n+{sx})+m-{sy} 와 만나는 두 점 중 x좌표가 작은 점을 C 라 할 때, "
        f"세 점 A, B, C 가 다음 조건을 만족시킨다. "
        f"(가) 직선 AC 와 직선 y={ps}x 는 서로 수직이다. "
        f"(나) 삼각형 AOB 와 삼각형 ACB 의 넓이의 비는 {r.p}:{r.q} 이다. "
        f"m+n 의 최댓값을 구하시오. (단, O 는 원점이다.)"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
