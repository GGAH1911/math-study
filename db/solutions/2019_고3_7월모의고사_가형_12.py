import sympy as sp

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# f(1)=f1, f'(1)=fp1 이고 h(x)=(g∘f)(x) 일 때
#   (나) lim_{x->1} (h(x)-h1)/(x-1) = hp1
# 는 h(1)=h1, h'(1)=hp1 을 뜻한다.
#   h(1) = g(f(1)) = g(f1) = h1                → g(f1) = h1
#   h'(1) = g'(f(1))·f'(1) = g'(f1)·fp1 = hp1   → g'(f1) = hp1 / fp1   (연쇄법칙, sympy solve 로 계산)
# 답은 g(f1) + g'(f1).
#
# 답을 바꾸는 파라미터: fp1, h1, hp1 (value 계산에 직접 쓰임) · ch_start, ch_step (보기 목록을
#   옮기면 정답 값이 같은 보기 안에서도 다른 번호에 놓인다). f1 은 g 를 평가하는 지점을
#   지정할 뿐 (극한 조건에서 유도되는 값이 자체로 답이므로) 값 계산에는 관여하지 않는
#   문제 설정용 파라미터다.
#
# 보기는 원문제처럼 "공차가 있는 등차수열"로 고정된 창(ch_start, ch_step, n_choices 로 결정)
# 이며 value(prm) 이 그 창을 벗어나면 이 문제 유형으로 성립하지 않으므로 예외를 던진다.

CANDIDATE = 3  # ★원문제 정답 (③)

PARAMS = dict(
    f1=2,        # f(1) — g 를 평가하는 지점 (문제 설정값, 답 계산엔 직접 안 쓰임)
    fp1=3,       # f'(1)
    h1=5,        # 조건 (나)의 극한식이 뜻하는 h(1) 값
    hp1=12,      # 조건 (나)의 극한값, 즉 h'(1)
    ch_start=5,  # 보기 ①의 값
    ch_step=2,   # 보기 사이 공차 → 보기 목록 = ①5 ②7 ③9 ④11 ⑤13
    n_choices=5,
)


def value(prm):
    """g(f1) + g'(f1) 을 sympy 로 실제 계산.

    h(1)=g(f(1))=h1, h'(1)=g'(f(1))·f'(1)=hp1 이라는 두 방정식을
    sympy.solve 로 풀어 g(f1), g'(f1) 을 구한다(연쇄법칙 그대로).
    """
    G, Gp = sp.symbols('G Gp')  # G = g(f1), Gp = g'(f1)
    h1 = sp.nsimplify(prm['h1'])
    hp1 = sp.nsimplify(prm['hp1'])
    fp1 = sp.nsimplify(prm['fp1'])
    eq1 = sp.Eq(G, h1)               # h(1) = g(f(1))
    eq2 = sp.Eq(Gp * fp1, hp1)       # h'(1) = g'(f(1))·f'(1)  (연쇄법칙)
    sol = sp.solve([eq1, eq2], [G, Gp])
    if not sol:
        raise ValueError('조건을 만족하는 g(f1), g\'(f1) 이 없다')
    return sp.nsimplify(sol[G] + sol[Gp])


def choices(prm):
    """보기 목록: ch_start 에서 시작해 ch_step 씩 커지는 등차수열 n_choices 개."""
    return [sp.nsimplify(prm['ch_start'] + i * prm['ch_step']) for i in range(int(prm['n_choices']))]


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    for i, c in enumerate(ch, start=1):
        if sp.simplify(v - c) == 0:
            return i
    raise ValueError(f'값 {v}이(가) 보기 {ch}에 없음 — 이 문제 유형으로 성립하지 않음')


def statement(prm):
    ch = choices(prm)
    body = (
        "실수 전체의 집합에서 미분가능한 두 함수 f(x), g(x)에 대하여 함수 h(x)를 "
        "h(x)=(g \\circ f)(x) 라 할 때, 두 함수 f(x), h(x)가 다음 조건을 만족시킨다.\n"
        f"(가) f(1)={prm['f1']} , f'(1)={prm['fp1']}\n"
        f"(나) \\lim_{{x \\to 1}} \\frac{{h(x)-{prm['h1']}}}{{x-1}}={prm['hp1']}\n"
        f"g({prm['f1']})+g'({prm['f1']})의 값은?"
    )
    return body + '  보기: ' + ' '.join(f'{i}) {v}' for i, v in enumerate(ch, start=1))


# 원문제 보기가 정확히 ①5 ②7 ③9 ④11 ⑤13 인지 고정 검증
assert choices(PARAMS) == [5, 7, 9, 11, 13]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
