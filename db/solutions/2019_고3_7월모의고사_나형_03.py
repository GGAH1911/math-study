import sympy as sp

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# lim_{n→∞} (A n^2 + Bn n) / (C n^2 + Dc) = A/C  (분자·분모를 n^2 으로 나누면
# 1차항·상수항은 0으로 사라지고 최고차항 계수의 비 A/C 만 남는다).
#   - A, C : 최고차항 계수 → 극한값 A/C 를 실제로 결정한다.
#   - Bn, Dc : 1차항·상수항 계수 → 극한에는 영향 없지만 문제 문장 구성에 쓰인다.
#   - unit  : 보기들의 공차(간격). 보기는 unit, 2·unit, 3·unit, 4·unit, 5·unit 로
#             등간격 배치되고, 극한값 A/C 가 그중 몇 번째(k·unit)인지가 정답 번호다.
# A, C, unit 은 서로 묶여 있다: A/C 가 unit 의 정수배이면서 1~5 배 범위 안에 들어야
# 보기 중 하나와 정확히 일치하는 '성립하는' 문제가 된다. 그래서 개별 파라미터를 하나만
# 흔들면(예: A 만 +1) 그 조건이 깨지기 쉬우므로 VARIANTS 로 성립하는 조합을 제시한다.

CANDIDATE = 5  # ★원문제 정답(보기 번호), 절대 바꾸지 않음

PARAMS = dict(A=5, Bn=-1, C=2, Dc=1, unit=sp.Rational(1, 2))


def value(prm):
    """lim_{n→∞} (A n^2 + Bn n)/(C n^2 + Dc) 를 sympy 로 실제 계산."""
    n = sp.Symbol('n')
    A, Bn, C, Dc = prm['A'], prm['Bn'], prm['C'], prm['Dc']
    if C == 0:
        raise ValueError('분모의 최고차항 계수가 0이면 문제가 성립하지 않는다')
    expr = (A * n**2 + Bn * n) / (C * n**2 + Dc)
    v = sp.limit(expr, n, sp.oo)
    if not v.is_number or v.has(sp.zoo, sp.nan, sp.oo, -sp.oo):
        raise ValueError(f'극한값이 유한한 수가 아니다: {v}')
    return sp.nsimplify(v)


def choices(prm):
    """값에서 유도한 5지 선다: unit, 2·unit, 3·unit, 4·unit, 5·unit."""
    u = sp.nsimplify(prm['unit'])
    if u <= 0:
        raise ValueError('보기 간격은 양수여야 한다')
    return [u * k for k in range(1, 6)]


def solve(prm):
    """값이 보기 중 정확히 몇 번째(1~5)에 오는지 찾아 보기 번호를 반환."""
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f'값 {v} 이 보기 {ch} 안에 없다 — 성립하지 않는 조합')
    return ch.index(v) + 1


# 원문제 보기 재현 확인: ① 1/2 ② 1 ③ 3/2 ④ 2 ⑤ 5/2
assert choices(PARAMS) == [sp.Rational(1, 2), sp.Integer(1), sp.Rational(3, 2),
                            sp.Integer(2), sp.Rational(5, 2)]


def statement(prm):
    n = sp.Symbol('n')
    A, Bn, C, Dc = prm['A'], prm['Bn'], prm['C'], prm['Dc']
    num = sp.latex(A * n**2 + Bn * n)
    den = sp.latex(C * n**2 + Dc)
    ch = choices(prm)
    circ = ['①', '②', '③', '④', '⑤']
    opts = ' '.join(f'{c} \\frac{{{sp.latex(sp.fraction(x)[0])}}}{{{sp.latex(sp.fraction(x)[1])}}}'
                     if sp.fraction(x)[1] != 1 else f'{c} {sp.latex(x)}'
                     for c, x in zip(circ, ch))
    return (f"\\lim_{{n \\to \\infty}} \\frac{{{num}}}{{{den}}} 의 값은? [2점]\n"
            f"  {opts}")


# ── 성립하는 조합들: (A, Bn, C, Dc, unit) 이 서로 묶여 있어 하나만 흔들면
#    A/C 가 unit 의 정수배·1~5배 범위 조건이 깨지므로, 성립하는 조합을 직접 제시 ──
VARIANTS = [
    dict(A=5, Bn=-1, C=2, Dc=1, unit=sp.Rational(1, 2)),   # 원문제: 5/2 → 5번
    dict(A=3, Bn=2, C=2, Dc=-5, unit=sp.Rational(1, 2)),   # 3/2 → 3번
    dict(A=1, Bn=4, C=1, Dc=7, unit=sp.Rational(1, 2)),    # 1   → 2번
    dict(A=4, Bn=0, C=1, Dc=3, unit=sp.Integer(1)),        # 4   → 4번
]

if __name__ == '__main__':
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
