"""2019 고3 10월모의고사 가형 22번 — 파라미터 솔버.

문제: 서로 다른 n개에서 r개를 뽑는 "중복조합" H(n,r) 의 값을 구하시오.
수학 구조: 중복조합 H(n,r) = C(n+r-1, r) 이고, 이는 (n-1)개의 구분자와 r개의
공을 일렬로 배열하는 경우의 수와 같다 (막대와 별 방법).
n(서로 다른 종류의 개수)과 r(뽑는 개수)이 문제를 정하는 두 파라미터이며,
둘 다 답을 실제로 바꾼다.
"""
import sympy as sp

CANDIDATE = 84  # ★원문제 정답, 절대 변경 금지

PARAMS = dict(
    n=7,  # 서로 다른 종류의 개수
    r=3,  # 중복을 허용하여 뽑는 개수
)


def solve(prm):
    n, r = prm['n'], prm['r']
    if not (isinstance(n, int) and isinstance(r, int) and n >= 1 and r >= 0):
        raise ValueError("n은 1 이상의 정수, r은 0 이상의 정수여야 합니다.")
    # 중복조합 H(n,r) = C(n+r-1, r) 을 sympy 이항계수로 실제 계산
    N, R = sp.Integer(n), sp.Integer(r)
    value = sp.binomial(N + R - 1, R)
    return int(value)


def statement(prm):
    n, r = prm['n'], prm['r']
    return f"서로 다른 {n}개의 종류에서 중복을 허용하여 {r}개를 택하는 중복조합의 수 " \
           f"_{{{n}}}H_{{{r}}} 의 값을 구하시오."


if __name__ == '__main__':
    # 원문제 재현 확인
    assert solve(PARAMS) == CANDIDATE

    # 파라미터가 답을 실제로 바꾸는지 확인 (장식 파라미터가 아님을 검증)
    changed_by_n = solve(dict(n=8, r=3)) != solve(dict(n=7, r=3))
    changed_by_r = solve(dict(n=7, r=4)) != solve(dict(n=7, r=3))
    assert changed_by_n, "n을 바꿔도 답이 그대로임"
    assert changed_by_r, "r을 바꿔도 답이 그대로임"

    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
