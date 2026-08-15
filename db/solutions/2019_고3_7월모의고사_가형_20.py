import sympy as sp

CANDIDATE = 5  # ★원문제 정답(⑤ ㄱ,ㄴ,ㄷ). 절대 바꾸지 않는다.

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# f 는 x=1, x=2 에 대해 대칭 → 주기 2 인 함수(항상 성립하는 일반 정리, ㄱ).
# 대표해로 f(x) = A - C*cos(pi*x) 를 쓰면 두 대칭조건을 자동으로 만족한다.
#   f(1)-f(0) = 2C  →  ∫_2^5 f'(x)dx = D1 조건에서 C = D1/2 로 결정.
#   ㄴ 은 "f(1)-f(0)=L2" 라는 진술이므로 L2 == D1 일 때만 참.
#   ∫_0^1 f(f(x))f'(x)dx = ∫_{f(0)}^{f(1)} f(u)du = D2 (u=f(x) 치환) 에서 A 결정.
#   ㄷ 은 "∫_1^U f(x)dx = L3" 라는 진술이므로 실제 계산값과 L3 이 같을 때만 참.
# D1 이 짝수여야 C 가 정수가 되어 sin(pi*C)=0 로 깔끔한 닫힌해가 나온다(원문제도 C=2).
PARAMS = dict(
    D1=4,               # ∫_2^5 f'(x)dx 의 값
    D2=6,                # ∫_0^1 f(f(x))f'(x)dx 의 값 (ㄷ 가정)
    U=10,                 # ∫_1^U f(x)dx 의 상한
    L2=4,                # ㄴ이 주장하는 f(1)-f(0) 의 값
    L3=sp.Rational(27, 2),  # ㄷ이 주장하는 ∫_1^U f(x)dx 의 값
)

# 원문제의 5개 보기(고정된 조합 목록 — 3명제 중 그럴듯한 조합만 뽑아둔 표준 형태)
CHOICE_DEFS = [
    ('ㄱ',),
    ('ㄷ',),
    ('ㄱ', 'ㄴ'),
    ('ㄴ', 'ㄷ'),
    ('ㄱ', 'ㄴ', 'ㄷ'),
]
assert CHOICE_DEFS[4] == ('ㄱ', 'ㄴ', 'ㄷ')  # 원문제 정답 ⑤의 내용 고정


def _core(prm):
    """sympy 로 실제 대수/적분을 풀어 (ga, nb, dc, actual) 을 구한다."""
    D1, D2, U, L2, L3 = prm['D1'], prm['D2'], prm['U'], prm['L2'], prm['L3']
    D1, D2, U = sp.nsimplify(D1), sp.nsimplify(D2), sp.nsimplify(U)
    L2, L3 = sp.nsimplify(L2), sp.nsimplify(L3)

    if D1 == 0 or not D1.is_integer or D1 % 2 != 0:
        raise ValueError('D1 은 0이 아닌 짝수 정수여야 닫힌해가 존재한다')
    if not U.is_integer:
        raise ValueError('U 는 정수여야 한다')

    A, u, x = sp.symbols('A u x')
    C = sp.Rational(D1, 2)          # ∫_2^5 f'(x)dx=D1, f(1)-f(0)=2C=D1
    f_u = A - C * sp.cos(sp.pi * u)  # 대칭조건 f(1+t)=f(1-t), f(2+t)=f(2-t) 를 만족하는 대표해

    f0, f1 = f_u.subs(u, 0), f_u.subs(u, 1)          # f(0), f(1)
    lhs2 = sp.integrate(f_u, (u, f0, f1))            # u=f(x) 치환으로 얻은 ∫_0^1 f(f(x))f'(x)dx
    sols = sp.solve(sp.Eq(lhs2, D2), A)
    if not sols:
        raise ValueError('주어진 D2 로 A 를 구할 수 없음')
    A_val = sols[0]

    actual = sp.integrate(f_u.subs(A, A_val), (u, 1, U))   # 실제 ∫_1^U f(x)dx
    actual = sp.simplify(actual)

    ga = True                                    # 주기성(ㄱ)은 대칭조건에서 항상 성립하는 일반 정리
    nb = sp.simplify(L2 - D1) == 0                # ㄴ: f(1)-f(0)=L2 가 실제 D1 과 같은가
    dc = sp.simplify(actual - L3) == 0            # ㄷ: 진술한 L3 이 실제 계산값과 같은가
    return ga, nb, dc, actual, A_val


def value(prm):
    """수학적 답: 어떤 보기(ㄱ,ㄴ,ㄷ)가 참인지의 조합."""
    ga, nb, dc, _, _ = _core(prm)
    combo = tuple(lbl for lbl, ok in zip(('ㄱ', 'ㄴ', 'ㄷ'), (ga, nb, dc)) if ok)
    return combo


def choices(prm):
    return CHOICE_DEFS


def solve(prm):
    combo = value(prm)
    opts = choices(prm)
    if combo not in opts:
        raise ValueError(f'참인 보기 조합 {combo} 이 주어진 선택지에 없음')
    return opts.index(combo) + 1


def statement(prm):
    D1, D2, U, L2, L3 = prm['D1'], prm['D2'], prm['U'], prm['L2'], prm['L3']
    return (
        "실수 전체의 집합에서 미분가능한 함수 f(x)가 모든 실수 x에 대하여 "
        "f(1+x)=f(1-x), f(2+x)=f(2-x) 를 만족시킨다. 실수 전체의 집합에서 f'(x)가 "
        f"연속이고, \\int_{{2}}^{{5}} f'(x)dx = {D1}일 때, <보기>에서 옳은 것만을 있는 대로 고른 것은?\n"
        "<보기>\n"
        "ㄱ. 모든 실수 x에 대하여 f(x+2)=f(x) 이다.\n"
        f"ㄴ. f(1)-f(0)={L2}\n"
        f"ㄷ. \\int_{{0}}^{{1}} f(f(x))f'(x)dx = {D2}일 때, \\int_{{1}}^{{{U}}} f(x)dx = {sp.nsimplify(L3)}이다.\n"
        "① ㄱ ② ㄷ ③ ㄱ, ㄴ ④ ㄴ, ㄷ ⑤ ㄱ, ㄴ, ㄷ"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
