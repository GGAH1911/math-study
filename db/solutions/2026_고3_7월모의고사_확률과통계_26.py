# 2026 고3 7월 확률과통계 26번 — 파라미터화 솔버
#
# 구조: X~N(m,σ²).
#   ① P(m≤X≤2m)=p_mid  →  P(0≤Z≤m/σ)=p_mid  →  m/σ = z1      (표 역참조)
#   ② P(X≥a)=p_tail     →  (a-m)/σ = za                        (표 역참조, p_tail>1/2 면 za<0)
#   ①②를 연립해 σ = a/(z1+za), m = z1σ 를 실제로 풀고,
#   ③ P(lo≤X≤hi) 를 표준화해 표준정규분포표로 조립 → 보기와 대조.
# 숫자(a·p_mid·p_tail·lo·hi·표·보기)를 바꾸면 같은 유형의 새 문제가 된다.
import sympy as sp

CANDIDATE = 3

R = sp.Rational

# 문제가 준 표준정규분포표: z → P(0≤Z≤z)
STD_TABLE = {R(1, 2): R(1915, 10000), R(1): R(3413, 10000),
             R(3, 2): R(4332, 10000), R(2): R(4772, 10000)}

PARAMS = dict(
    a=2,                        # P(X ≥ a) 의 기준점
    p_mid=R(4772, 10000),       # P(m ≤ X ≤ 2m)
    p_tail=R(8413, 10000),      # P(X ≥ a)
    lo=0,                       # 구하려는 구간의 왼쪽 끝
    hi=5,                       # 구하려는 구간의 오른쪽 끝
    table=STD_TABLE,            # 표준정규분포표
    choices=[R(5328, 10000), R(6247, 10000), R(6687, 10000),
             R(6826, 10000), R(7745, 10000)],   # ①~⑤ 보기 값 (정답 번호는 solve 가 정한다)
)


def _phi_half(z, table):
    """P(0 ≤ Z ≤ |z|). 표에 있으면 표값(문제가 의도한 값), 없으면 오차함수로 계산해 소수 넷째자리 반올림."""
    zz = sp.Abs(sp.nsimplify(z))
    if zz in table:
        return table[zz]
    return R(int(round(float(sp.erf(zz / sp.sqrt(2)) / 2) * 10000)), 10000)


def _z_from_half(p, table):
    """P(0 ≤ Z ≤ z) = p 를 만족하는 z. 표 역참조 우선, 없으면 수치 역함수."""
    p = sp.nsimplify(p)
    if not (0 < p < R(1, 2)):
        raise ValueError(f'표 확률 범위를 벗어남: {p}')
    for z, v in table.items():
        if sp.simplify(v - p) == 0:
            return z
    return R(int(round(float(sp.sqrt(2) * sp.erfinv(2 * sp.Float(p))) * 10 ** 6)), 10 ** 6)


def _interval_prob(zl, zh, table):
    """P(zl ≤ Z ≤ zh) 를 표(대칭성) 로 조립."""
    zl, zh = sp.nsimplify(zl), sp.nsimplify(zh)
    if zl > zh:
        zl, zh = zh, zl
    if zl >= 0:
        return _phi_half(zh, table) - _phi_half(zl, table)
    if zh <= 0:
        return _phi_half(zl, table) - _phi_half(zh, table)
    return _phi_half(zl, table) + _phi_half(zh, table)


def moments(prm):
    """두 조건을 연립해 (m, σ) 를 실제로 푼다."""
    z1 = _z_from_half(prm['p_mid'], prm['table'])          # m/σ
    p_tail = sp.nsimplify(prm['p_tail'])
    if p_tail > R(1, 2):
        za = -_z_from_half(p_tail - R(1, 2), prm['table'])  # (a-m)/σ < 0
    else:
        za = _z_from_half(R(1, 2) - p_tail, prm['table'])   # (a-m)/σ > 0
    mu, sg = sp.symbols('mu sigma', positive=True)
    sol = sp.solve([sp.Eq(mu / sg, z1), sp.Eq((prm['a'] - mu) / sg, za)], [mu, sg], dict=True)
    if not sol:
        raise ValueError('조건을 만족하는 정규분포가 없음')
    return sol[0][mu], sol[0][sg]


def prob(prm):
    """P(lo ≤ X ≤ hi) 의 값."""
    m0, s0 = moments(prm)
    return _interval_prob((prm['lo'] - m0) / s0, (prm['hi'] - m0) / s0, prm['table'])


def solve(prm=None, a=2, lo=0, hi=5, **kw):
    """조건 → 정답 보기 번호. 보기에 없으면 0."""
    P = dict(PARAMS)
    P.update(a=a, lo=lo, hi=hi)
    P.update(kw)
    if prm:
        P.update(prm)
    val = prob(P)
    for i, c in enumerate(P['choices'], 1):
        if sp.simplify(val - sp.nsimplify(c)) == 0:
            return i
    return 0


def statement(prm=None):
    """같은 유형의 새 문제 문장."""
    P = dict(PARAMS)
    if prm:
        P.update(prm)
    rows = ' / '.join(f'{float(z)}→{float(v):.4f}' for z, v in sorted(P['table'].items()))
    ch = ' '.join(f'{n} {float(c):.4f}' for n, c in
                  zip('①②③④⑤', P['choices']))
    return (f"정규분포 N(m, σ²)을 따르는 확률변수 X에 대하여\n"
            f"  P(m ≤ X ≤ 2m) = {float(P['p_mid']):.4f},  P(X ≥ {P['a']}) = {float(P['p_tail']):.4f}\n"
            f"일 때, P({P['lo']} ≤ X ≤ {P['hi']}) 의 값을 표준정규분포표\n"
            f"  [z → P(0≤Z≤z)]  {rows}\n"
            f"를 이용하여 구한 것은?\n  {ch}")


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
