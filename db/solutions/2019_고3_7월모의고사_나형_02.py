from sympy import symbols, Eq, solve as sp_solve

CANDIDATE = 3  # 원문제 정답: 선택지 ③ (실제 값은 a+b=6)

# 문제 구조:
#   A = {p1, a+k, p2},  B = {b, q1, q2},  A∩B = {target}
#   ⇒ (a+k = target, b = target) 를 sympy 로 풀면 a = target-k, b = target.
#   선택지 5개는 흔히 나올 법한 '오답' 값들을 오름차순 정렬한 목록이고,
#   실제 정답(a+b)이 그 목록에서 몇 번째(①~⑤)인지가 채점 대상이다.
#     v1 = a                (b를 안 더한 실수)
#     v2 = b                (a를 안 더한 실수)
#     v3 = a+b               ← 진짜 정답
#     v4 = p1+p2             (A의 나머지 두 원소를 더해버린 실수)
#     v5 = q1+q2-target       (B의 나머지 두 원소에서 교집합값을 뺀 실수)
#   target·k는 A∩B={target} 조건 자체를 결정하므로 값(v3)과 순위(선택지 번호)를
#   둘 다 바꾸는 핵심 변수이고, p1,p2,q1,q2는 나머지 두 원소(교집합과는 무관해야
#   하며, 겹치면 조건이 깨져 예외가 난다) 겸 오답 보기 생성에 쓰인다.
PARAMS = dict(
    p1=3,       # A의 고정 원소1
    p2=5,       # A의 고정 원소2
    k=2,        # A의 변동 원소 = a + k  (원문제: a+2)
    target=4,   # 교집합 값, A∩B = {target}
    q1=6,       # B의 고정 원소1
    q2=8,       # B의 고정 원소2
)


def _solve_ab(prm):
    """A∩B = {target} 조건(a+k=target, b=target)을 sympy 로 실제로 푼다."""
    a, b = symbols('a b', real=True)
    k, target = prm['k'], prm['target']
    a_sol = sp_solve(Eq(a + k, target), a)[0]
    b_sol = sp_solve(Eq(b, target), b)[0]
    return a_sol, b_sol


def _validate(prm, a_sol, b_sol):
    """A = {p1, a+k, p2}, B = {b, q1, q2} 를 실제 집합으로 만들어
    교집합이 정확히 {target} 인지 확인한다. 아니면 이 파라미터 조합은
    '두 집합의 교집합이 {target}' 이라는 문제 전제 자체가 성립하지 않는다."""
    p1, p2, k, target, q1, q2 = (prm['p1'], prm['p2'], prm['k'], prm['target'],
                                  prm['q1'], prm['q2'])
    A = {p1, a_sol + k, p2}
    B = {b_sol, q1, q2}
    if A & B != {target}:
        raise ValueError(f'A∩B가 {{{target}}}가 되지 않는다: A={A}, B={B}')


def value(prm):
    """수학적으로 실제 정답인 a+b 값."""
    a_sol, b_sol = _solve_ab(prm)
    _validate(prm, a_sol, b_sol)
    return a_sol + b_sol


def choices(prm):
    """정답 값에서 유도한 5지선다 보기(오름차순 정렬)."""
    a_sol, b_sol = _solve_ab(prm)
    _validate(prm, a_sol, b_sol)
    p1, p2, k, target, q1, q2 = (prm['p1'], prm['p2'], prm['k'], prm['target'],
                                  prm['q1'], prm['q2'])
    v1 = a_sol
    v2 = b_sol
    v3 = a_sol + b_sol
    v4 = p1 + p2
    v5 = q1 + q2 - target
    return sorted({v1, v2, v3, v4, v5})


def solve(prm):
    """정답이 보기 목록에서 몇 번째(①=1 ... ⑤=5)인지 돌려준다."""
    a_sol, b_sol = _solve_ab(prm)
    _validate(prm, a_sol, b_sol)
    v = a_sol + b_sol
    ch = choices(prm)
    return ch.index(v) + 1


def statement(prm):
    p1, p2, k, target, q1, q2 = (prm['p1'], prm['p2'], prm['k'], prm['target'],
                                  prm['q1'], prm['q2'])
    ch = choices(prm)
    labels = ['①', '②', '③', '④', '⑤']
    opts = ' '.join(f'{lab} {c}' for lab, c in zip(labels, ch))
    return (
        f'두 집합 A = {{{p1}, a+{k}, {p2}}}, B = {{b, {q1}, {q2}}}에 대하여 '
        f'A ∩ B = {{{target}}}일 때, a+b의 값은? (단, a, b는 실수이다.)\n{opts}'
    )


assert choices(PARAMS) == [2, 4, 6, 8, 10], choices(PARAMS)  # 원문제 보기와 동일해야 함

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
