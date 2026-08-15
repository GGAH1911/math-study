import sympy as sp

CANDIDATE = 3  # ★원문제 정답 (③) — 절대 변경 금지

# 문제 구조: log_a(p) + log_a(q) 꼴의 로그 합을, 로그의 합 법칙으로 log_a(p*q) 로 묶어
# 계산하는 문제다. 원문제는 log_2 3 + log_2 (8/3) 로, p*q = 3 * 8/3 = 8 = 2^3 이 되도록
# 설계되어 있어 밑이 2인 로그값이 깔끔한 정수 3 이 된다.
#   base   : 로그의 밑
#   p, q   : 두 로그의 진수 (분수여도 됨)
#   anchor : 보기 5개(연속한 정수)의 시작값 — 원문제는 ①1 ②2 ③3 ④4 ⑤5 이므로 1
PARAMS = dict(base=2, p=sp.Integer(3), q=sp.Rational(8, 3), anchor=1)


def value(prm):
    """log_base(p) + log_base(q) 를 실제로 sympy 로 계산한 값 (로그 합의 법칙 적용)."""
    base, p, q = prm['base'], prm['p'], prm['q']
    expr = sp.log(p, base) + sp.log(q, base)
    v = sp.simplify(expr)
    if not v.is_number or v.has(sp.zoo, sp.nan, sp.oo, sp.I):
        raise ValueError(f'유효하지 않은 답: {v}')
    return v


def choices(prm):
    """anchor 부터 시작하는 연속한 정수 5개 (원문제 보기: ①1 ②2 ③3 ④4 ⑤5)."""
    a = prm['anchor']
    return [sp.Integer(a) + i for i in range(5)]


def solve(prm):
    """값을 구하고, 그 값이 보기 중 몇 번째(①=1 ... ⑤=5)인지 반환한다.

    값이 정수가 아니거나 보기 범위(anchor..anchor+4) 밖이면 그 조합은 문제로
    성립하지 않으므로 예외를 던진다.
    """
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f'값 {v} 이 보기 {ch} 안에 없다 — 문제로 성립하지 않음')
    return ch.index(v) + 1


# 원문제 파라미터로 만든 보기가 실제 원문제 보기 [1,2,3,4,5] 와 같은지 고정
assert choices(PARAMS) == [1, 2, 3, 4, 5]


def statement(prm):
    base, p, q = prm['base'], prm['p'], prm['q']
    ch = choices(prm)
    opts = ' '.join(f'{sym} {c}' for sym, c in zip('①②③④⑤', ch))
    return (
        f"\\log_{{{base}}} {sp.latex(sp.nsimplify(p))} + "
        f"\\log_{{{base}}} {sp.latex(sp.nsimplify(q))}의 값은?\n"
        f"{opts}"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
