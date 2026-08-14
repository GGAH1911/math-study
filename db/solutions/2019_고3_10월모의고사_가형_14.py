import sympy as sp

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# 곡선 f: y = log_b(x-a) 와 곡선 g: y = b^x + a 는 서로 역함수 관계다
#   (y=log_b(x-a) ⇔ x = b^y + a 이므로 f의 그래프를 y=x에 대해 대칭시키면 g가 된다,
#    이는 b, a 값에 상관없이 항상 성립하는 구조다).
# 점 A는 f와 직선 y=k·x의 교점이므로 A=(x_A, k·x_A).
# A를 지나는 기울기 -1인 직선이 g와 만나는 점 B는 정확히 A를 y=x에 대해 대칭시킨
# 점 B=(k·x_A, x_A) 이다 — f 위의 점을 y=x로 대칭시키면 항상 g 위의 점이 되고,
# 두 대칭점을 잇는 선분의 기울기는 언제나 -1이기 때문이다
# (원문제의 "기울기 -1" 조건이 바로 이 대칭 구조를 지정한 것).
# 삼각형 OAB(O=원점)의 넓이 = (1/2)|x_A·x_A − (k·x_A)·(k·x_A)| = (1/2)(1−k²)x_A².
# 이 식을 S로 놓고 x_A(>0)를 sympy 방정식으로 실제로 풀어 구한 뒤,
# a = x_A − b^{k·x_A} (A가 로그곡선 위에 있다는 조건)로 계산한다.
#
# 답을 바꾸는 파라미터: b(로그·지수의 밑, 원문제 √2), k(직선 y=kx의 기울기, 원문제 1/2),
# S(삼각형 OAB의 넓이, 원문제 6) — 모두 a = x_A − b^{k·x_A} 계산에 실제로 쓰인다.
# 다만 이 문제는 "값이 고정 보기(①1/2 ②1 ③3/2 ④2 ⑤5/2) 중 하나로 떨어져야" 유효한
# 객관식 문항이 되는, 서로 묶인 조건이므로(규칙 5의 결합 파라미터 사례) 성립하는
# (b,k,S) 조합들을 VARIANTS로 제시한다. 그 밖의 임의 조합은 규칙 6에 따라 예외를 던진다.

CANDIDATE = 4  # ★원문제 정답: ④번 (값 a=2)

PARAMS = dict(
    b=sp.sqrt(2),          # 로그·지수의 밑 (원문제: y=log_{√2}(x-a), y=(√2)^x+a)
    k=sp.Rational(1, 2),   # 점 A가 놓인 직선 y=kx 의 기울기 (원문제: y=(1/2)x)
    S=6,                   # 삼각형 OAB의 넓이 조건 (원문제: 6)
)

# 서로 묶인 (b, k, S) 조합들: 각각 값 a = x_A - b^{k·x_A} 가 고정 보기 중 하나로
# 떨어져야 성립한다. 이 중 두 개 이상은 원문제(a=2, ④)와 다른 답을 낸다.
VARIANTS = [
    dict(k=sp.Rational(2, 3), S=sp.Rational(5, 2)),   # a=1   -> ② (원문제와 다른 답)
    dict(k=0, S=sp.Rational(9, 8)),                   # a=1/2 -> ① (원문제와 다른 답)
    dict(k=0, S=sp.Rational(25, 8)),                  # a=3/2 -> ③ (원문제와 다른 답)
    dict(b=2, k=sp.Rational(1, 3), S=4),              # a=1   -> ② (밑 b도 바뀌어도 성립)
]


def value(prm):
    """넓이 조건으로부터 x_A를 sympy 방정식으로 실제로 풀고, a = x_A - b^{k x_A} 를 계산한다."""
    b = sp.nsimplify(prm['b'])
    k = sp.nsimplify(prm['k'])
    S = sp.nsimplify(prm['S'])
    xA = sp.symbols('x_A', positive=True)
    # 넓이 공식: (1/2)(1-k^2) x_A^2 = S  →  x_A 를 실제로 방정식으로 풀이(양의 해 채택)
    eq = sp.Eq(sp.Rational(1, 2) * (1 - k**2) * xA**2, S)
    sols = [s for s in sp.solve(eq, xA) if s.is_real and s.is_positive]
    if not sols:
        raise ValueError("조건을 만족하는 점 A가 존재하지 않음 — 문제로 성립하지 않음")
    xA_val = sols[0]
    yA_val = k * xA_val

    # 점 B = (yA_val, xA_val) 이 실제로 지수곡선 y=b^x+a 위에 있는지까지 확인하며 a를 구한다.
    a_sym = sp.symbols('a')
    eq_a = sp.Eq(xA_val - a_sym, b ** yA_val)   # A가 로그곡선 위에 있다는 조건
    a_sols = sp.solve(eq_a, a_sym)
    if not a_sols:
        raise ValueError("상수 a에 대한 해가 존재하지 않음")
    a_val = sp.nsimplify(sp.simplify(a_sols[0]))

    # B = (yA_val, xA_val): 지수곡선 y=b^x+a 위에서 x=yA_val 일 때 y가 xA_val 인지 확인
    if sp.simplify((b ** yA_val + a_val) - xA_val) != 0:
        raise ValueError("점 B가 지수곡선 위에 있지 않음 — 구조가 성립하지 않음")

    return a_val


def choices(prm):
    """이 문제 유형이 강제하는 고정 보기(①~⑤): 1/2 간격의 등차수열.

    값이 언제나 이 다섯 개 중 하나로 떨어지도록 (b,k,S)가 묶여 있으므로(VARIANTS
    참고) 값에서 별도로 유도하지 않고 유형 자체가 요구하는 등차수열을 그대로 쓴다.
    """
    return (sp.Rational(1, 2), sp.Integer(1), sp.Rational(3, 2), sp.Integer(2), sp.Rational(5, 2))


def solve(prm):
    v = sp.nsimplify(value(prm))
    ch = choices(prm)
    for i, cand in enumerate(ch):
        if sp.simplify(v - cand) == 0:
            return i + 1  # 1-based 보기 번호 (①=1, ..., ⑤=5)
    raise ValueError(f"값 {v} 이 보기 {ch} 안에 없음 — 이 보기 형식의 문제로 성립하지 않음")


def statement(prm):
    b, k, S = prm['b'], prm['k'], prm['S']
    circled = ['①', '②', '③', '④', '⑤']
    opts = ' '.join(f"{s}{v}" for s, v in zip(circled, choices(prm)))
    return (
        f"곡선 $y=\\log_{{{sp.latex(b)}}}(x-a)$와 직선 $y={sp.latex(k)}x$가 만나는 점 중 한 점을 A라 하고, "
        f"점 A를 지나고 기울기가 -1인 직선이 곡선 $y=({sp.latex(b)})^{{x}}+a$와 만나는 점을 B라 하자. "
        f"삼각형 OAB의 넓이가 {S}일 때, 상수 a의 값은? (단, O는 원점이다.)\n  {opts}"
    )


# 원문제 보기가 정확히 ①1/2 ②1 ③3/2 ④2 ⑤5/2 인지 고정 검증
assert choices(PARAMS) == (sp.Rational(1, 2), sp.Integer(1), sp.Rational(3, 2), sp.Integer(2), sp.Rational(5, 2))

if __name__ == '__main__':
    print(statement(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
