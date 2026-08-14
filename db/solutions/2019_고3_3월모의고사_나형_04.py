"""2019 고3 3월모의고사 나형 4번 — 파라미터화 솔버.

원문제: X = {1,2,3,4,5} 위의 함수 f : X → X 가 그림(순열 대응)으로 주어지고,
(f∘f)(3) 의 값을 구하는 문제. (정답 ⑤ = 5)

수학 구조:
  - f 는 유한집합 X = {1,...,n} 위의 순열(bijection)이다.
  - 물어보는 것은 f 를 k 번 합성한 값 (f∘f∘...∘f)(x), 즉 f^k(x) 이다.
    원문제는 k=2 (f∘f).
  - sympy.combinatorics.Permutation 으로 f 를 실제 순열 객체로 만들고
    p**k 로 k 번 합성한 뒤 x 에서의 값을 계산한다 (숫자를 직접 반환하지 않음).
  - 답은 항상 X 의 원소이므로 보기(①~⑤)는 X = {1,...,n} 그 자체이고,
    선택지 번호는 '값이 X 를 정렬한 목록에서 몇 번째인가'로 정해진다.

파라미터화한 것:
  - perm : f 의 대응표 (f(1),...,f(n)) — 그림에서 읽은 순열. 이걸 바꾸면
           합성 결과가 통째로 달라진다.
  - x    : (f∘...∘f) 를 적용할 시작점. 바꾸면 답이 달라진다.
  - k    : 합성 횟수 (원문제는 f∘f 이므로 k=2). 바꾸면 답이 달라진다.
  - n    : 정의역/공역의 크기 (= |X|), 보기 개수와 연동된다.
"""

from sympy.combinatorics import Permutation

CANDIDATE = 5  # 원문제 정답: 보기 ⑤ 의 값 5   ★절대 바꾸지 않음

PARAMS = dict(
    n=5,
    perm=[4, 5, 2, 1, 3],  # 그림에서 읽은 대응: f(1)=4, f(2)=5, f(3)=2, f(4)=1, f(5)=3
    x=3,                    # (f∘f)(3) 을 구하라
    k=2,                    # f 를 2번 합성 (f∘f)
)


def _check_permutation(perm, n):
    if sorted(perm) != list(range(1, n + 1)):
        raise ValueError(f"perm={perm} 은 1..{n} 의 순열이 아닙니다.")


def value(prm):
    """f 를 k번 합성한 뒤 x 에 적용한 값 f^k(x) 를 sympy 순열 연산으로 계산."""
    n, perm, x, k = prm["n"], prm["perm"], prm["x"], prm["k"]
    _check_permutation(perm, n)
    if not (1 <= x <= n):
        raise ValueError(f"x={x} 는 정의역 1..{n} 범위를 벗어납니다.")
    if k < 1:
        raise ValueError("k(합성 횟수)는 1 이상이어야 합니다.")

    # f : X -> X 를 0-인덱스 배열형 순열로 구성 (sympy Permutation)
    p = Permutation([img - 1 for img in perm])
    q = p ** k  # f 를 k번 합성한 순열 (실제 sympy 연산으로 계산)
    return q(x - 1) + 1  # 다시 1-인덱스로 환산


def choices(prm):
    """보기는 X = {1,...,n} 자체 (합성 결과가 항상 X 의 원소이므로)."""
    return tuple(range(1, prm["n"] + 1))


def solve(prm):
    """value(prm) 이 choices(prm) 중 몇 번째(①=1, ..., ⑤=5)인지 반환."""
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f"value={v} 가 보기 {ch} 안에 없습니다.")
    return ch.index(v) + 1


def statement(prm):
    n, perm, x, k = prm["n"], prm["perm"], prm["x"], prm["k"]
    mapping = ", ".join(f"f({i})={perm[i-1]}" for i in range(1, n + 1))
    comp = "∘".join(["f"] * k)
    return (
        f"집합 X = {{{', '.join(str(i) for i in range(1, n + 1))}}} 에 대하여 "
        f"함수 f : X → X 가 {mapping} 로 주어져 있다. "
        f"({comp})({x}) 의 값은?\n"
        + "  ".join(f"{['①','②','③','④','⑤','⑥','⑦','⑧','⑨'][i-1]} {c}" for i, c in enumerate(choices(prm), start=1))
    )


# 원문제의 보기(①1 ②2 ③3 ④4 ⑤5)와 유도된 보기가 일치하는지 고정
assert choices(PARAMS) == (1, 2, 3, 4, 5)

if __name__ == "__main__":
    print(statement(PARAMS))
    print("value:", value(PARAMS), "choice:", solve(PARAMS))

    # 파라미터를 바꾸면 실제로 답이 달라지는지 확인
    import copy

    p_x = copy.deepcopy(PARAMS)
    p_x["x"] = 1
    print("x=1 일 때 값:", value(p_x))  # 1 (원본과 다름)

    p_k = copy.deepcopy(PARAMS)
    p_k["k"] = 1
    print("k=1 일 때 값:", value(p_k))  # 2 (원본과 다름)

    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
