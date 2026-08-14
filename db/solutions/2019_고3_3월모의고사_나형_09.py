# -*- coding: utf-8 -*-
"""
[원문제]
두 집합 A = {1,2,3,4}, B = {3,4,5,6}에 대하여
  A ∩ X = A,  X ∪ (A ∪ B) = A ∪ B
를 만족시키는 집합 X의 개수는?
① 1 ② 2 ③ 4 ④ 8 ⑤ 16   (정답 ③)

[수학 구조]
- 조건 A ∩ X = A  ⇔  A ⊆ X
- 조건 X ∪ (A∪B) = A∪B  ⇔  X ⊆ A∪B
- 종합하면 A ⊆ X ⊆ A∪B, 즉 X = A ∪ Y (Y ⊆ (A∪B)\\A = B\\A)
- 조건을 만족하는 X의 개수는 (B\\A)의 부분집합 개수인 2^|B\\A| 개.
  ⇒ 문제를 실제로 결정하는 파라미터는 집합 A, B 자체(정확히는 |B\\A|)이다.
- 이 유형(수능/모평 "부분집합 개수" 문제)의 보기는 관례적으로 2^0, 2^1, ..., 2^4
  (=1,2,4,8,16) 다섯 개로 주어지므로, |B\\A| ∈ {0,1,2,3,4} 범위에서 성립한다.
"""

from sympy import FiniteSet
from sympy.utilities.iterables import subsets

CANDIDATE = 3  # ★원문제 정답 (보기 번호, 절대 변경 금지)

# 문제를 결정하는 두 집합. 실제로 답을 바꾸는 파라미터는 A, B 두 개이며,
# 특히 두 집합의 차집합 크기 |B\A| 가 정답을 좌우한다.
PARAMS = dict(
    A=(1, 2, 3, 4),
    B=(3, 4, 5, 6),
)


def _check_condition(A, B, X):
    """원문제의 두 조건을 그대로 검증: A∩X=A, X∪(A∪B)=A∪B."""
    union_AB = A | B
    return (A & X) == A and (X | union_AB) == union_AB


def value(prm):
    """조건을 만족하는 집합 X의 개수를 실제로 전수조사(부분집합 열거)로 구한다."""
    A = FiniteSet(*prm["A"])
    B = FiniteSet(*prm["B"])
    universe = sorted({int(e) for e in (A | B)})

    if len(universe) > 12:
        # 전수조사 시간 폭주 방지 (2^12 = 4096 이므로 여유롭게 제한)
        raise ValueError("전체집합이 너무 커서 전수조사를 40초 안에 마칠 수 없습니다.")

    Aset, Bset = set(prm["A"]), set(prm["B"])
    count = 0
    for r in range(len(universe) + 1):
        for combo in subsets(universe, r):  # sympy.utilities.iterables.subsets 로 전수조사
            X = set(combo)
            if _check_condition(Aset, Bset, X):
                count += 1
    return count


def choices(prm):
    """
    이 유형 문제의 표준 보기: 2^0, 2^1, 2^2, 2^3, 2^4 (=1,2,4,8,16).
    실제 값(value)이 이 범위를 벗어나면(= |B\\A| 가 0~4 밖) 문제로 성립하지 않으므로
    solve()에서 예외를 던진다.
    """
    return [2 ** i for i in range(5)]


# 유도한 보기가 원문제의 보기(①1 ②2 ③4 ④8 ⑤16)와 같은지 고정
assert choices(PARAMS) == [1, 2, 4, 8, 16]


def solve(prm):
    """조건을 만족하는 X의 개수를 구하고, 그 값이 몇 번 보기인지(1-indexed) 반환."""
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f"계산된 값 {v}가 보기 {ch} 범위를 벗어납니다 (문제로 성립하지 않음).")
    return ch.index(v) + 1


def statement(prm):
    A = prm["A"]
    B = prm["B"]
    A_str = "{" + ", ".join(str(x) for x in A) + "}"
    B_str = "{" + ", ".join(str(x) for x in B) + "}"
    ch = choices(prm)
    ch_str = " ".join(f"{i+1}) {c}" for i, c in enumerate(ch))
    return (
        f"두 집합 A = {A_str}, B = {B_str}에 대하여\n"
        f"  A ∩ X = A, X ∪ (A ∪ B) = A ∪ B\n"
        f"를 만족시키는 집합 X의 개수는?\n"
        f"{ch_str}"
    )


if __name__ == "__main__":
    print(statement(PARAMS))
    print("계산된 값(value):", value(PARAMS))
    print("보기(choices):", choices(PARAMS))
    print("solve(PARAMS):", solve(PARAMS))

    # --- 파라미터 민감도 확인: A, B를 각각 바꿔 답이 실제로 달라지는지 검증 ---
    variant_B = dict(A=PARAMS["A"], B=(2, 3))  # B\A = {} -> |B\A|=0 -> value=1 -> 1번
    variant_A = dict(A=(1, 2, 3), B=(3, 4, 5, 6, 7))  # B\A={4,5,6,7} -> |B\A|=4 -> value=16 -> 5번
    print("A 변경 시 solve:", solve(variant_A), "(value=", value(variant_A), ")")
    print("B 변경 시 solve:", solve(variant_B), "(value=", value(variant_B), ")")
    assert solve(variant_A) != solve(PARAMS)
    assert solve(variant_B) != solve(PARAMS)
    assert solve(variant_A) != solve(variant_B)

    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
