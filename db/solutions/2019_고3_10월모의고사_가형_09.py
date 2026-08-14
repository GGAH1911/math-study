# [원문제] 모든 실수 x에 대하여 f(x)>0인 연속함수 f(x)에 대하여
#   ∫_a^b f(x)dx = I 일 때, 곡선 y=f(mx+k) 와 x축 및 두 직선 x=x1, x=x2 로
#   둘러싸인 부분의 넓이는?
#
# [수학 구조] 치환 u = m·x + k (du = m·dx) 를 쓰면
#   ∫_{x1}^{x2} f(m x + k) dx = (1/m) ∫_{a}^{b} f(u) du = I/m
#   단, 치환이 유효하려면 x=x1 일 때 u=a, x=x2 일 때 u=b 여야 하므로
#   a = m·x1 + k, b = m·x2 + k (파라미터가 서로 묶여 있음 → a,b 는 PARAMS 로
#   직접 흔들지 않고 m,k,x1,x2 로부터 유도해서 항상 일관되게 만든다).
#
# [파라미터화] 답을 실제로 바꾸는 손잡이는 I(적분값)와 m(치환 배율) 두 개
#   — 넓이 = I/m 이라는 구조 자체가 이 두 값에만 의존한다. x1,x2,k 는
#   구간·평행이동 등 문제 겉모습만 바꾸고 값에는 영향이 없다.
#   보기(choices)는 원문제의 실제 보기를 그대로 담아 두고, 계수를 바꿔 값이
#   그 목록 밖으로 나가면(=새 보기가 필요한 변형) solve 가 보기 번호 대신
#   값 자체를 반환한다.

import sympy as sp

CANDIDATE = 2  # ★원문제 정답: ②

PARAMS = dict(
    x1=1, x2=2,          # 넓이를 구하는 x 구간 [x1, x2]
    m=2, k=1,             # 치환 u = m x + k  → y = f(m x + k)
    I=36,                  # ∫_a^b f(u) du = I  (a,b 는 m,k,x1,x2 로 유도)
    choices=[sp.Integer(16), sp.Integer(18), sp.Integer(20),
             sp.Integer(22), sp.Integer(24)],   # 보기 ①~⑤
)


def bounds(prm):
    """치환이 유효하도록 a=m*x1+k, b=m*x2+k 를 유도. (묶인 파라미터)"""
    m, k, x1, x2 = prm['m'], prm['k'], prm['x1'], prm['x2']
    if m == 0:
        raise ValueError('m=0 이면 치환이 되지 않는다')
    a = m * x1 + k
    b = m * x2 + k
    if b == a:
        raise ValueError('구간 길이가 0')
    return a, b


def value(prm):
    """구하는 넓이 = ∫_{x1}^{x2} f(mx+k) dx 를 치환을 이용해 실제로 sympy 로 푼다."""
    bounds(prm)  # 치환의 유효성(적분 구간 대응)을 확인
    m, I = prm['m'], prm['I']
    J = sp.symbols('J')  # J = 구하려는 넓이
    # 치환 u=mx+k, du=m dx 로부터 I = ∫_a^b f(u)du = m·∫_{x1}^{x2} f(mx+k)dx = m·J
    eq = sp.Eq(m * J, sp.nsimplify(I))
    sol = sp.solve(eq, J)
    if not sol:
        raise ValueError('해가 없음')
    return sp.nsimplify(sol[0])


def solve(prm):
    """보기 번호를 반환. 값이 보기 목록 밖이면(=새 보기가 필요한 변형) 값 자체를 반환."""
    v = value(prm)
    for i, c in enumerate(prm['choices'], 1):
        if sp.simplify(v - sp.nsimplify(c)) == 0:
            return i
    return v


def statement(prm):
    a, b = bounds(prm)
    m, k, x1, x2, I = prm['m'], prm['k'], prm['x1'], prm['x2'], prm['I']
    ksign = f'+{k}' if k > 0 else (f'{k}' if k < 0 else '')
    ch_str = ' '.join(f'{n}{sp.nsimplify(c)}' for n, c in zip('①②③④⑤', prm['choices']))
    return (
        f'모든 실수 x에 대하여 f(x)>0인 연속함수 f(x)에 대하여 '
        f'∫_{{{a}}}^{{{b}}} f(x)dx={I} 일 때, 곡선 y=f({m}x{ksign})과 x축 및 두 직선 '
        f'x={x1}, x={x2}로 둘러싸인 부분의 넓이는?  {ch_str}'
    )


# 원문제 보기가 그대로 재현되는지 고정
assert [int(c) for c in PARAMS['choices']] == [16, 18, 20, 22, 24]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
