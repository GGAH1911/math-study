import sympy as sp

# ----------------------------------------------------------------------
# 원문제 구조: 자연수 n 이하의 원소들로 이루어진 집합 A의 부분집합 중,
#   - 처음 m개의 원소(1, 2, ..., m)를 반드시 포함하고
#   - 전체 원소 개수가 홀수인
# 부분집합의 개수를 구하는 문제.
#
# 나머지 (n-m)개의 원소에서 j개를 자유롭게 고르면 부분집합의 크기는 m+j이므로,
# m+j가 홀수가 되도록 j의 홀짝을 맞춰 고르는 경우의 수를 세면 된다.
# 이항계수의 홀수/짝수 항 합은 대칭이므로 그 값은 항상 2^(n-m-1) (n-m>=1일 때).
#
# 보기는 2^K, 2^(K+1), ..., 2^(K+4) (원문제 기준 K=18) 5개짜리 고정 창(window)이고,
# n, m을 바꾸면 정답 지수 e = n-m-1 이 이 창 안에서 이동해 정답 번호(①~⑤)가 실제로 바뀐다.
# ----------------------------------------------------------------------

CANDIDATE = 5

PARAMS = dict(
    n=25,   # 집합 A = {1, 2, ..., n}의 원소 개수
    m=2,    # 반드시 포함해야 하는 원소(1, 2, ..., m)의 개수
    K=18,   # 보기 5개의 시작 지수 (2^K ~ 2^(K+4)), 원문제의 보기 구성
)


def value(prm):
    """정답의 수학적 값: 조건을 만족하는 부분집합의 개수를 sympy로 직접 계산."""
    n, m = prm['n'], prm['m']
    if m < 0 or n <= m:
        raise ValueError("m은 0 이상이고 n보다 작아야 합니다.")
    rest = n - m  # 자유롭게 선택 가능한 원소 개수
    if rest < 1:
        raise ValueError("자유 원소가 없어 홀짝 대칭 논리가 성립하지 않습니다.")

    total = sp.Integer(0)
    # 부분집합 크기 = m + j 가 홀수가 되도록 하는 j에 대해 이항계수를 실제로 합산
    for jj in range(rest + 1):
        if (m + jj) % 2 == 1:
            total += sp.binomial(rest, jj)
    total = sp.nsimplify(total)

    # 홀짝 대칭성에 의한 닫힌 식과 일치하는지 내부 검증(문제 구조 확인용)
    closed_form = sp.Integer(2) ** (rest - 1)
    if sp.simplify(total - closed_form) != 0:
        raise AssertionError("이항계수 합과 닫힌 식이 불일치합니다.")
    return total


def choices(prm):
    """보기 5개: 2^K, 2^(K+1), ..., 2^(K+4). K를 기준으로 값에서 유도."""
    K = prm['K']
    return [sp.Integer(2) ** (K + i) for i in range(5)]


def solve(prm):
    v = value(prm)
    cs = choices(prm)
    if v not in cs:
        raise ValueError(f"정답 {v}가 보기 범위 {cs} 밖에 있어 문제가 성립하지 않습니다.")
    return cs.index(v) + 1


def statement(prm):
    n, m = prm['n'], prm['m']
    cs = choices(prm)
    labels = ['①', '②', '③', '④', '⑤']
    opts = ' '.join(f"{labels[i]} {cs[i]}" for i in range(5))
    mandatory = ', '.join(str(i) for i in range(1, m + 1))
    return (
        f"집합 A = {{x | x는 {n} 이하의 자연수}}의 부분집합 중 "
        f"원소 {mandatory}을 모두 포함하고 원소의 개수가 홀수인 부분집합의 개수는? "
        f"{opts}"
    )


# 원문제 보기(2^18~2^22)가 그대로 유도되는지 고정 검증
assert choices(PARAMS) == [sp.Integer(2) ** e for e in range(18, 23)]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
