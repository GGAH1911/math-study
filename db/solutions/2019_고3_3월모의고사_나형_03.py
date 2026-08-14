from sympy import FiniteSet

# ── 원문제 ───────────────────────────────────────────────────────────
# 두 집합 A = {2,3,4}, B = {3,4,5,6} 에 대하여 n(A∩B) 의 값은?
# ① 1 ② 2 ③ 3 ④ 4 ⑤ 5   → 정답 ② (값 2)
#
# ── 파라미터화한 수학 구조 ───────────────────────────────────────────
# 이 문제의 답은 두 유한집합 A, B 에 의해 완전히 결정된다.
#   - 값(정답의 실체) = n(A∩B)  : A, B의 교집합의 원소 개수
#   - 보기 목록      = 1 부터 (|A|+|B|-2) 까지의 자연수
#     (두 집합의 크기만으로 "그럴듯한 개수 보기"를 정하는 자연스러운 상한이며,
#      교집합의 크기는 항상 min(|A|,|B|) 이하이므로 이 범위 안에 반드시 포함된다)
#   - solve()가 돌려주는 것은 "보기 번호"(①=1, ②=2, ...) 이며,
#     이는 value(prm)이 choices(prm) 안에서 몇 번째인지로 결정된다.
# A, B 를 바꾸면 (a) 교집합 원소 개수(value)가 바뀌고 (b) 집합의 크기가 바뀌어
# 보기 목록의 길이도 바뀌므로, 결과적으로 solve()가 돌려주는 보기 번호 자체가
# A만 바꿔도, B만 바꿔도 각각 독립적으로 달라진다.

CANDIDATE = 2  # ★원문제 정답(② → 값 2). 절대 바꾸지 않음.

PARAMS = dict(
    A=(2, 3, 4),        # 집합 A의 원소들
    B=(3, 4, 5, 6),      # 집합 B의 원소들
)


def value(prm):
    """A∩B 의 원소 개수 n(A∩B) 를 sympy FiniteSet 으로 실제 계산."""
    A = FiniteSet(*prm['A'])
    B = FiniteSet(*prm['B'])
    inter = A.intersect(B)
    return len(inter)


def choices(prm):
    """값에서 유도된 보기 목록: 1 부터 |A|+|B|-2 까지의 자연수."""
    A, B = prm['A'], prm['B']
    upper = len(A) + len(B) - 1  # range()의 배타적 상한
    if upper < 2:
        raise ValueError("집합이 너무 작아 보기를 구성할 수 없습니다.")
    ch = tuple(range(1, upper))
    v = value(prm)
    if v not in ch:
        raise ValueError("교집합의 크기가 보기 범위를 벗어나 문제로 성립하지 않습니다.")
    return ch


# 유도한 보기가 원문제의 보기(①1 ②2 ③3 ④4 ⑤5)와 같은지 고정
assert choices(PARAMS) == (1, 2, 3, 4, 5)


def solve(prm):
    """정답 값이 보기 목록에서 몇 번째(①,②,...)인지를 반환."""
    ch = choices(prm)
    v = value(prm)
    return ch.index(v) + 1


def statement(prm):
    A, B = prm['A'], prm['B']
    A_str = ', '.join(str(x) for x in A)
    B_str = ', '.join(str(x) for x in B)
    ch = choices(prm)
    circled = "①②③④⑤⑥⑦⑧⑨⑩"
    opts = ' '.join(f"{circled[i]} {c}" for i, c in enumerate(ch))
    return (
        f"두 집합 A = \\{{{A_str}\\}}, B = \\{{{B_str}\\}}에 대하여 "
        f"n(A \\cap B)의 값은? [2점]\n  {opts}"
    )


if __name__ == "__main__":
    print(statement(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')

    # 파라미터를 바꾸면 답(보기 번호)이 실제로 달라지는지 확인
    v1 = dict(A=(2, 3, 4, 5), B=(3, 4, 5, 6))       # A만 변경
    v2 = dict(A=(2, 3, 4), B=(3, 5, 6, 7))          # B만 변경
    print("A만 변경:", solve(v1), "(값:", value(v1), ", 보기:", choices(v1), ")")
    print("B만 변경:", solve(v2), "(값:", value(v2), ", 보기:", choices(v2), ")")
    assert solve(v1) != CANDIDATE
    assert solve(v2) != CANDIDATE
    assert solve(v1) != solve(v2)
