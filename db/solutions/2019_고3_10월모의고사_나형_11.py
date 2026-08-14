import sympy as sp

CANDIDATE = 4  # ★원문제 정답(보기 번호): 절대 바꾸지 않음

PARAMS = dict(
    mu=5, sigma=2,          # X ~ N(mu, sigma^2)
    # 등식 P(X<=p-q*a) = P(X>=r*a-s) 의 계수들 (lo=p-q*a, hi=r*a-s)
    p=9, q=2,
    r=3, s=3,
    # 표준정규분포표 (문제에 주어진 표, z -> P(0<=Z<=z))
    table={sp.Rational(1, 1): sp.Rational(3413, 10000),
           sp.Rational(3, 2): sp.Rational(4332, 10000),
           sp.Rational(2, 1): sp.Rational(4772, 10000),
           sp.Rational(5, 2): sp.Rational(4938, 10000)},
)


def value(prm):
    """P(lo<=X<=hi) 를 실제로 sympy 로 계산."""
    mu, sigma = sp.Rational(prm['mu']), sp.Rational(prm['sigma'])
    p, q, r, s = (sp.Rational(prm[k]) for k in ('p', 'q', 'r', 's'))
    table = prm['table']

    a = sp.symbols('a', real=True)
    # 대칭조건: P(X<=lo)=P(X>=hi) <=> lo+hi = 2*mu (정규분포의 평균 대칭성)
    lo_expr = p - q * a
    hi_expr = r * a - s
    sols = sp.solve(sp.Eq(lo_expr + hi_expr, 2 * mu), a)
    if len(sols) != 1:
        raise ValueError("a에 대한 해가 유일하지 않습니다.")
    av = sols[0]

    lo = lo_expr.subs(a, av)
    hi = hi_expr.subs(a, av)
    if hi <= lo:
        raise ValueError("hi<=lo: 구간이 성립하지 않습니다.")

    z_lo = sp.nsimplify((lo - mu) / sigma)
    z_hi = sp.nsimplify((hi - mu) / sigma)
    # 대칭 조건에 의해 z_lo = -z_hi 여야 함
    if sp.simplify(z_lo + z_hi) != 0:
        raise ValueError("구간이 평균에 대해 대칭이지 않습니다.")
    if z_hi <= 0:
        raise ValueError("z_hi<=0 입니다.")
    if z_hi not in table:
        raise ValueError(f"z_hi={z_hi} 가 표에 없는 값입니다.")

    return 2 * table[z_hi], z_hi


def choices(prm):
    """표의 네 z값(z0<z1<z2<z3)으로 만든 5개 보기.
    ①pair(z0,z1) ②double(z1) ③pair(z1,z2) ④double(z2) ⑤double(z3)
    -> 원문제 보기 구성과 동일한 함정 패턴(표에서 값 조회 실수)."""
    table = prm['table']
    zs = sorted(table.keys())
    if len(zs) != 4:
        raise ValueError("표는 정확히 4개의 z값을 가져야 합니다.")
    z0, z1, z2, z3 = zs
    c = [
        table[z0] + table[z1],
        2 * table[z1],
        table[z1] + table[z2],
        2 * table[z2],
        2 * table[z3],
    ]
    return [float(x) for x in c]


def solve(prm):
    val, z_hi = value(prm)
    cs = choices(prm)
    valf = float(val)
    for i, c in enumerate(cs, start=1):
        if abs(c - valf) < 1e-9:
            return i
    raise ValueError(f"계산된 값 {valf} 이 보기 중에 없습니다.")


def statement(prm):
    mu, sigma = prm['mu'], prm['sigma']
    p, q, r, s = prm['p'], prm['q'], prm['r'], prm['s']
    zs = sorted(prm['table'].keys())
    table_rows = "\n".join(f"    {z} : {float(prm['table'][z])}" for z in zs)
    return (
        f"확률변수 X가 정규분포 N({mu}, {sigma}^2)을 따를 때, "
        f"등식 P(X <= {p}-{q}a) = P(X >= {r}a-{s}) 을 만족시키는 상수 a에 대하여 "
        f"P({p}-{q}a <= X <= {r}a-{s})의 값을 아래 표준정규분포표를 이용하여 구한 것은?\n"
        f"[표]\n{table_rows}"
    )


# 원문제 보기와 일치하는지 고정 검증
_orig_choices = choices(PARAMS)
assert [round(x, 4) for x in _orig_choices] == [0.7745, 0.8664, 0.9104, 0.9544, 0.9876], _orig_choices

# p, s 는 실제로 답을 바꾸는 파라미터: (p,s)를 함께 흔들면 대칭점 a가 바뀌고
# 그 결과 z_hi가 표의 다른 z값으로 이동해 정답 보기 번호가 달라진다.
VARIANTS = [
    dict(PARAMS, p=10, s=4),  # z_hi=1.5 -> 보기 ②(0.8664)
    dict(PARAMS, p=9, s=3),   # 원문제 그대로 -> 보기 ④(0.9544)
    dict(PARAMS, p=8, s=2),   # z_hi=2.5 -> 보기 ⑤(0.9876)
]
_variant_answers = [solve(v) for v in VARIANTS]
assert len(set(_variant_answers)) >= 2, _variant_answers  # 서로 다른 답이 실제로 나오는지 확인

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
