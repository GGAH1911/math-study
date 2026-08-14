import sympy as sp

# [원문제]
# 실수 전체의 집합에서 미분가능한 두 함수 f(x), g(x)에 대하여 h(x)=(f∘g)(x)라 하자.
#   lim_{x->1} (g(x)+1)/(x-1) = 2,   lim_{x->1} (h(x)-2)/(x-1) = 12
# 일 때, f(-1)+f'(-1)의 값은?  ① 4 ② 5 ③ 6 ④ 7 ⑤ 8   → 정답 ⑤(=5번)
#
# [수학 구조]
#   두 극한이 모두 "0/0" 꼴이라야 극한값이 유한하다.
#   lim (g(x)+c1)/(x-a) = L1  ⇒ g(a) = -c1, g'(a) = L1
#   lim (h(x)-c2)/(x-a) = L2  ⇒ h(a) = c2,  h'(a) = L2
#   연쇄법칙: h'(a) = f'(g(a))·g'(a) = f'(-c1)·L1 = L2  ⇒  f'(-c1) = L2/L1
#   또한 h(a) = f(g(a)) = f(-c1) = c2
#   구하는 값 = f(-c1) + f'(-c1) = c2 + L2/L1
#
# 파라미터로 뽑은 것: a(극한점), c1(=g(x)의 이동량), c2(=h(x)의 목표값), L1, L2(두 극한값)
# 답을 실제로 바꾸는 것: c1, c2, L1, L2 (a 는 문제 서술상의 극한점일 뿐 값 구조엔 영향 없음)

CANDIDATE = 5  # ①~⑤ 중 정답 번호 (수식값 8 = 다섯 번째 보기 ⑤)

PARAMS = dict(a=1, c1=1, c2=2, L1=2, L2=12)


def value(prm):
    """f(-c1) + f'(-c1) 의 실제 값 (연쇄법칙으로 계산)."""
    c1 = sp.nsimplify(prm['c1'])
    c2 = sp.nsimplify(prm['c2'])
    L1 = sp.nsimplify(prm['L1'])
    L2 = sp.nsimplify(prm['L2'])
    if L1 == 0:
        # g'(a)=L1=0 이면 연쇄법칙으로 f'(-c1)을 유일하게 결정할 수 없다 → 문제 성립 X
        raise ValueError("L1(=g'(a))이 0이면 f'(-c1)을 구할 수 없어 문제가 성립하지 않는다")
    return c2 + L2 / L1


def choices(prm):
    """보기 5개: 정답 1개 + 연쇄법칙 일부를 빠뜨리거나 값을 혼동한 오답 4개 (모두 value 에서 유도)."""
    c1 = sp.nsimplify(prm['c1'])
    c2 = sp.nsimplify(prm['c2'])
    L1 = sp.nsimplify(prm['L1'])
    L2 = sp.nsimplify(prm['L2'])
    if L1 == 0:
        raise ValueError("L1이 0이면 문제가 성립하지 않는다")
    v = value(prm)
    w1 = c2 + L1            # f'(-c1) 자리에 L1 을 그대로 대입한 오답
    w2 = c1 + c2 + L1       # c1 을 불필요하게 더한 오답
    w3 = L2 / L1            # f(-c1)(=c2) 더하는 것을 빠뜨린 오답
    w4 = c1 + L2 / L1       # f(-c1) 대신 c1 을 사용한 오답
    opts = sorted({v, w1, w2, w3, w4})
    if len(opts) != 5:
        raise ValueError("보기 중 값이 겹쳐 5지선다가 성립하지 않는다")
    return tuple(opts)


# 원문제의 보기(①4 ②5 ③6 ④7 ⑤8)가 그대로 유도되는지 고정
assert choices(PARAMS) == (4, 5, 6, 7, 8)


def solve(prm):
    """value(prm) 이 choices(prm) 중 몇 번째 보기인지 반환."""
    opts = choices(prm)
    v = value(prm)
    return opts.index(v) + 1


def statement(prm):
    a, c1, c2, L1, L2 = prm['a'], prm['c1'], prm['c2'], prm['L1'], prm['L2']
    opts = choices(prm)
    marks = ['①', '②', '③', '④', '⑤']
    opt_str = ' '.join(f'{m} {o}' for m, o in zip(marks, opts))
    return (
        "실수 전체의 집합에서 미분가능한 두 함수 f(x), g(x)에 대하여 "
        "함수 h(x)를 h(x)=(f∘g)(x)라 하자.\n"
        f"lim_{{x→{a}}} (g(x)+{c1})/(x-{a}) = {L1},  "
        f"lim_{{x→{a}}} (h(x)-{c2})/(x-{a}) = {L2}\n"
        f"일 때, f(-{c1})+f'(-{c1})의 값은?\n{opt_str}"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
