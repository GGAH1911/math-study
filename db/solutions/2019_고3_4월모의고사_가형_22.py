"""2019 고3 4월모의고사 가형 22번 — 파라미터 솔버.

문제: ₂Π₅ (중복순열) 의 값을 구하시오.

수학 구조: 서로 다른 n개에서 r개를 뽑아 만드는 중복순열의 수는
    ₙΠᵣ = n^r
이다. 원문제는 n=2, r=5 인 경우로 ₂Π₅ = 2^5 = 32.

파라미터화: n(원소 개수)과 r(뽑는 개수) 둘 다 답(2^r 값)을 실제로 바꾼다.
"""

import sympy as sp

CANDIDATE = 32  # ★원문제 정답. 바꾸지 않음.

# 문제를 정하는 값들: 서로 다른 n개에서 r개를 택하는 중복순열
PARAMS = dict(n=2, r=5)


def solve(prm):
    n, r = prm['n'], prm['r']
    n_s, r_s = sp.Integer(n), sp.Integer(r)

    if n_s < 1 or r_s < 1:
        raise ValueError("n, r 은 1 이상의 자연수여야 합니다.")

    # 중복순열의 수 ₙΠᵣ = n^r 을 sympy 로 직접 계산 (곱셈 원리:
    # r개의 자리 각각에 n개의 선택지가 독립적으로 곱해짐)
    result = sp.Integer(1)
    for _ in range(r_s):
        result *= n_s

    assert result == n_s ** r_s
    return int(result)


def statement(prm):
    n, r = prm['n'], prm['r']
    return f"₍{n}₎Π₍{r}₎의 값을 구하시오."


if __name__ == '__main__':
    # 원문제 재현 확인
    assert solve(PARAMS) == CANDIDATE

    # 파라미터를 바꾸면 답도 실제로 바뀌는지 확인 (장식 파라미터 아님)
    other1 = dict(n=3, r=4)   # 3^4 = 81 ≠ 32
    other2 = dict(n=2, r=6)   # 2^6 = 64 ≠ 32
    assert solve(other1) != CANDIDATE
    assert solve(other2) != CANDIDATE
    assert solve(other1) != solve(other2)

    print(statement(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
