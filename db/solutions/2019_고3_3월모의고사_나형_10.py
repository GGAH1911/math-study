import sympy as sp

# ------------------------------------------------------------------
# 문제의 수학 구조
#   log10( m^p / 10^(p*t) ) = a  라는 조건이 주어졌을 때
#   p*log10(m) 을 a 로 나타내면 항상   p*log10(m) = a + p*t
#   (m 은 소거되어 사라지고, 오프셋은 p*t 로만 결정된다.)
#
#   원문제: log 1.44 = a, 1.44 = 12^2/10^2  →  m=12, p=2, t=1
#           2 log 12 = a + 2*1 = a+2  →  보기 ①a+1 ②a+2 ③a+3 ④a+4 ⑤a+5 중 ②
#
# 파라미터
#   m : 로그를 취하는 밑수(12) - 문제 표면의 숫자, 답에는 영향 없음(장식)
#   p : 지수(제곱수, 원문제 2)      - 답을 바꾸는 핵심 파라미터
#   t : 10의 거듭제곱 지수(원문제 1) - 답을 바꾸는 핵심 파라미터
#   answer offset = p*t 가 1~5 사이에 있어야 보기 ①~⑤ 형식이 성립한다.
# ------------------------------------------------------------------

CANDIDATE = 2  # ★원문제 정답: ②

PARAMS = dict(m=12, p=2, t=1)


def _offset_via_sympy(p, t):
    """sympy로 log(m^p/10^(p t)) = a 조건에서 p*log10(m) 을 a로 표현해
    실제로 유도한다 (m은 소거됨을 대수적으로 확인)."""
    m_s = sp.Symbol('m', positive=True)
    u = sp.Symbol('u', positive=True)   # u = log10(m)
    a = sp.Symbol('a')

    term1 = sp.expand_log(sp.log(m_s**p, 10), force=True)              # log(m^p,10)
    term2 = sp.expand_log(sp.log(sp.Integer(10)**(p * t), 10), force=True)  # log(10^(pt),10)
    log_x_expr = (term1 - term2).subs(sp.log(m_s) / sp.log(10), u)     # log(x,10) as f(u)

    eq = sp.Eq(a, log_x_expr)               # 조건: a = log(x,10)
    sols = sp.solve(eq, u)                  # u(=log10 m)를 a로 풂
    if not sols:
        raise ValueError("u=log10(m)에 대한 해가 존재하지 않음")
    u_sol = sols[0]

    p_log_m = sp.expand(p * u_sol)          # p*log10(m) 을 a로 표현
    offset = sp.simplify(p_log_m - a)       # p*log10(m) - a  →  정수 오프셋
    if not offset.is_Integer:
        raise ValueError(f"오프셋이 정수가 아님: {offset}")
    return int(offset)


def value(prm):
    """문제의 수학적 답: p*log10(m) = a + offset 에서의 offset 값."""
    m, p, t = prm['m'], prm['p'], prm['t']
    if m <= 1 or p <= 0 or t <= 0:
        raise ValueError("m>1, p,t>0 인 정수여야 함")
    if m % 10 == 0:
        raise ValueError("m이 10의 배수면 소수 형태 문제가 자연스럽지 않음")
    return _offset_via_sympy(p, t)


def choices(prm):
    """원문제 보기 형식: a+1, a+2, a+3, a+4, a+5 (오프셋 1~5)."""
    return [1, 2, 3, 4, 5]


def solve(prm):
    off = value(prm)
    ch = choices(prm)
    if off not in ch:
        raise ValueError(f"오프셋 {off}가 보기 범위(1~5) 밖에 있어 문제가 성립하지 않음")
    return ch.index(off) + 1  # 1-based 보기 번호


def _decimal_str(m, p, t):
    """m^p / 10^(p*t) 를 유한소수 문자열로 표현."""
    num = m ** p
    d = p * t
    s = str(num).rjust(d + 1, '0')
    return s[:-d] + '.' + s[-d:]


def statement(prm):
    m, p, t = prm['m'], prm['p'], prm['t']
    x_str = _decimal_str(m, p, t)
    asked = f"{p}\\log {m}" if p != 1 else f"\\log {m}"
    ch = choices(prm)
    opts = " ".join(f"{n}" for n in ["①", "②", "③", "④", "⑤"])
    opt_lines = " ".join(
        f"{sym} a+{off}" for sym, off in zip(["①", "②", "③", "④", "⑤"], ch)
    )
    return (
        f"\\log {x_str} = a일 때, {asked}를 a로 나타낸 것은? [3점]\n"
        f"  {opt_lines}"
    )


# 원문제 보기(①a+1 ~ ⑤a+5)와 일치하는지 고정 검증
assert choices(PARAMS) == [1, 2, 3, 4, 5]

if __name__ == "__main__":
    print(statement(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')

    # 파라미터가 답을 실제로 바꾸는지 확인 (p, t 각각)
    variant_p = dict(m=45, p=2, t=2)   # offset = 2*2 = 4  -> ④
    variant_t = dict(m=7, p=1, t=3)    # offset = 1*3 = 3  -> ③
    print("변형(p,t 변경 offset=4):", solve(variant_p))
    print("변형(p,t 변경 offset=3):", solve(variant_t))
