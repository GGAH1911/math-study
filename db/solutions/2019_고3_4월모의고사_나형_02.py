# 원문제: 두 집합 A = {1, 3, 5}, B = {2, 3, 4} 에 대하여 A - B 의 모든 원소의 합은? (객관식 5지선다)
#
# 수학 구조 파라미터화:
#   - A, B  : 두 집합의 원소 목록. A - B (차집합) 를 sympy 로 실제 계산해 원소 합(value)을 구한다.
#   - base, step : 보기 ①~⑤ 가 이루는 등차수열의 시작값·공차. 원문제는 6,7,8,9,10 (base=6, step=1).
#     정답 선택지 번호는 "value 가 보기 수열의 몇 번째 항인가" 로 결정된다 — 즉 A, B 를 바꾸면
#     value 가 바뀌고, 그 값이 보기 수열의 다른 자리(혹은 바깥)로 이동하므로 정답 번호가 실제로 바뀐다.
#     (보기를 value 주위로 다시 짜맞추는 방식은 A/B 가 답에 아무 영향을 못 주는 장식이 되어 버리므로
#      금지 — 여기서는 보기 수열을 A/B 와 독립적으로 고정하고 value 가 그 안 어디에 들어가는지를 본다.)

from sympy import FiniteSet, Complement

CANDIDATE = 1  # ★원문제 정답: 선택지 ①

PARAMS = dict(
    A=[1, 3, 5],
    B=[2, 3, 4],
    base=6,   # 보기 수열의 첫 항
    step=1,   # 보기 수열의 공차
)

CIRCLED = ['①', '②', '③', '④', '⑤']


def value(prm):
    """A - B 의 모든 원소의 합을 sympy 집합 연산으로 구한다."""
    A = FiniteSet(*prm['A'])
    B = FiniteSet(*prm['B'])
    diff = Complement(A, B)
    if len(diff) == 0:
        raise ValueError('A - B 가 공집합 — 문제로 성립하지 않음')
    return sum(diff)


def choices(prm):
    """보기 ①~⑤: base 에서 시작해 step 씩 증가하는 등차수열 (value 와는 독립적으로 결정)."""
    base, step = prm['base'], prm['step']
    return [base + i * step for i in range(5)]


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f'value={v} 가 보기 {ch} 안에 없음 — 유효하지 않은 파라미터 조합')
    return ch.index(v) + 1  # 선택지 번호(1~5)


def statement(prm):
    A, B, ch = prm['A'], prm['B'], choices(prm)
    a_str = ', '.join(str(x) for x in A)
    b_str = ', '.join(str(x) for x in B)
    opts = ' '.join(f'{CIRCLED[i]} {c}' for i, c in enumerate(ch))
    return (f"두 집합 A = {{{a_str}}}, B = {{{b_str}}}에 대하여\n"
            f"  집합 A - B의 모든 원소의 합은?\n  {opts}")


# 원문제 보기(①6 ②7 ③8 ④9 ⑤10)가 그대로 재현되는지 고정
assert choices(PARAMS) == [6, 7, 8, 9, 10]

if __name__ == '__main__':
    print(statement(PARAMS))
    print(f'value = {value(PARAMS)}')
    print(f'선택지 = {choices(PARAMS)}')
    ans = solve(PARAMS)
    print(f'정답 = {CIRCLED[ans - 1]} ({ans})')
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
