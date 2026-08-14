import sympy as sp

# ---------------------------------------------------------------------------
# 원문제: 다섯 개의 문자 a, a, a, b, b 를 일렬로 나열하는 경우의 수는?
#   → 같은 것이 있는 순열: 전체 n개 중 종류별 개수(a_count, b_count, ...)가
#     같은 원소들의 자리를 서로 구별하지 않는 배열 수.
#     공식: n! / (a_count! · b_count! · ...)
#
# 파라미터화 포인트:
#   - a_count, b_count : 각 문자의 개수 (바꾸면 분모가 바뀌어 답이 바뀐다)
#   - n 은 a_count + b_count 로 종속(전체 문자 개수) — 별도로 흔들 필요 없음
# ---------------------------------------------------------------------------

CANDIDATE = 1  # ★원문제 정답: 보기 번호 ①(값 10) — problem.txt [정답] 1 그대로 (절대 바꾸지 않음)

PARAMS = dict(
    a_count=3,   # a 의 개수
    b_count=2,   # b 의 개수
)


def value(prm):
    """수학적 답: 같은 것이 있는 순열의 수 n!/(a!·b!)."""
    a_count = prm['a_count']
    b_count = prm['b_count']
    n = a_count + b_count
    return sp.factorial(n) / (sp.factorial(a_count) * sp.factorial(b_count))


def choices(prm):
    """보기 5개: 공차 step 등차수열, 정답 v 의 위치(pos)는 a_count·b_count 로 결정.

    원문제(a=3,b=2)에서는 pos=0 이 되어 정답이 ①번에 오도록 계수를 맞췄다.
    a_count·b_count 가 바뀌면 pos 도 바뀌어 정답 위치(보기 번호)가 실제로 이동한다
    → solve() 가 a_count·b_count 둘 다에 대해 살아있는 파라미터가 된다.
    """
    a_count = prm['a_count']
    b_count = prm['b_count']
    v = int(value(prm))
    step = max(1, v // 2)
    pos = (a_count - b_count - 1) % 5   # 정답이 등차수열에서 몇 번째(0-indexed)에 오는지
    return [v + (i - pos) * step for i in range(5)]


def solve(prm):
    """조건 → 보기 번호(1~5)."""
    v = value(prm)
    cs = choices(prm)
    return cs.index(v) + 1


def statement(prm):
    a_count = prm['a_count']
    b_count = prm['b_count']
    letters = ['a'] * a_count + ['b'] * b_count
    cs = choices(prm)
    circled = ['①', '②', '③', '④', '⑤']
    opts = ' '.join(f'{c}{n}' for c, n in zip(circled, cs))
    return (
        f"{a_count + b_count}개의 문자 {', '.join(letters)}를 일렬로 나열하는 경우의 수는? [2점]\n"
        f"  {opts}"
    )


# 원문제 보기가 실제로 ①10 ②15 ③20 ④25 ⑤30 인지 고정
assert choices(PARAMS) == [10, 15, 20, 25, 30]

print(statement(PARAMS))
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
