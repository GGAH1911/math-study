import sympy as sp

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# "1..n_faces 의 눈이 있는 주사위(그중 홀수 눈 n_odd 개)를 n_throws 번
#  던졌을 때, 나온 눈의 곱이 짝수일 확률" 을 구하는 문제.
#
# 곱이 짝수 ⟺ 적어도 한 번은 짝수 눈이 나옴 ⟺ 여사건("매번 홀수 눈")의 여집합
#   P(곱이 짝수) = 1 - (n_odd/n_faces)^n_throws
#
# 파라미터:
#   n_faces  : 주사위 눈금의 총 개수 (원문제: 6)
#   n_odd    : 그중 홀수 눈의 개수   (원문제: 3 → 홀/짝 비율 1/2)
#   n_throws : 던지는 횟수          (원문제: 5)
PARAMS = dict(n_faces=6, n_odd=3, n_throws=5)

CANDIDATE = 5  # 원문제 정답: 보기 ⑤ (31/32)


def _prob_all_odd(prm):
    """5번(=n_throws번) 모두 홀수 눈이 나올 확률 = (n_odd/n_faces)^n_throws."""
    n_faces, n_odd, n_throws = prm['n_faces'], prm['n_odd'], prm['n_throws']
    if not (0 < n_odd < n_faces):
        raise ValueError('홀수 눈의 개수는 1 이상이고 전체 눈금 수보다 작아야 한다')
    if n_throws < 1:
        raise ValueError('던지는 횟수는 1 이상이어야 한다')
    return sp.Rational(n_odd, n_faces) ** n_throws


def value(prm):
    """곱이 짝수일 실제 확률 (여사건 이용)."""
    return 1 - _prob_all_odd(prm)


def choices(prm):
    """보기 5개를 생성한다.

    수능형 문항은 흔히 정답의 분자(기약분수 A/D 의 A)를 기준으로 2씩 어긋난
    5개의 분자를 오답으로 배치한다. 그 범위가 0 미만(또는 D 초과)으로
    벗어나면, 정답이 범위의 맨 끝에 오도록 창을 밀어 만든다 — 원문제
    (A=1, D=32)가 정확히 이 경계 케이스라서 정답이 ⑤(맨 끝)에 있다.
    """
    p_odd = _prob_all_odd(prm)
    A, D = p_odd.p, p_odd.q
    if A - 4 < 0:
        window = [A, A + 2, A + 4, A + 6, A + 8]        # 정답이 창의 최솟값(=확률 최댓값)
    elif A + 4 > D:
        window = [A - 8, A - 6, A - 4, A - 2, A]         # 정답이 창의 최댓값(=확률 최솟값)
    else:
        window = [A - 4, A - 2, A, A + 2, A + 4]         # 정답이 창의 한가운데
    if window[0] < 0 or window[-1] > D:
        raise ValueError('유효한 보기 범위를 만들 수 없다 (n_throws 가 너무 작다)')
    # k(=곱이 홀수일 확률의 분자)가 클수록 곱이 짝수일 확률(1-k/D)은 작아지므로,
    # 보기를 오름차순(①→⑤)으로 배열하려면 k 는 내림차순으로 순회한다.
    return tuple(1 - sp.Rational(k, D) for k in reversed(window))


def solve(prm):
    """정답이 몇 번째 보기(1~5)인지 반환한다."""
    v = value(prm)
    for i, c in enumerate(choices(prm), start=1):
        if c == v:
            return i
    raise ValueError('정답이 보기 목록 안에 없다')


def statement(prm):
    n_faces, n_odd, n_throws = prm['n_faces'], prm['n_odd'], prm['n_throws']
    labels = '①②③④⑤'
    opts = ' '.join(f'{labels[i]} {c}' for i, c in enumerate(choices(prm)))
    return (
        f'1부터 {n_faces}까지의 눈이 있는 주사위(그중 홀수 눈이 {n_odd}개)를 '
        f'{n_throws}번 던져서 나오는 {n_throws}개의 눈의 수의 곱이 짝수일 확률은?\n'
        f'{opts}'
    )


# 원문제 보기 고정: ①23/32 ②25/32 ③27/32 ④29/32 ⑤31/32
_expected = tuple(sp.Rational(n, 32) for n in (23, 25, 27, 29, 31))
assert choices(PARAMS) == _expected, choices(PARAMS)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
