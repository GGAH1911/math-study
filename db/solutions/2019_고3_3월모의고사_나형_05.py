# 문제 구조:
#   첫째항 a1, 공비 r 인 등비수열의 무한급수 합 S = sum_{n=1}^{inf} a1*r^(n-1) 을
#   sympy로 실제 계산(summation)하고, 그 값 S 가 보기 다섯 개(연속한 정수, 시작값
#   choice_start 부터 5개) 중 몇 번째(①~⑤)에 위치하는지를 답으로 낸다.
#
# 파라미터화 포인트:
#   - a1 (첫째항), r (공비) : 이 둘이 실제 극한값 S = a1/(1-r) 을 결정한다.
#   - choice_start          : 보기 다섯 개(연속 정수)의 시작값. S 의 값 자체가
#                              아니라 보기 목록이 "어디서부터 시작하느냐"를 결정하므로,
#                              a1/r 이 같아도 choice_start 가 바뀌면 정답 번호가 바뀐다.
#   즉 a1, r, choice_start 셋 다 solve() 의 최종 반환값(보기 번호)을 실제로 바꾼다.
#   (원문제는 a1=3, r=1/2, choice_start=4 → 보기 [4,5,6,7,8] 중 6이 3번째 → ③)

from sympy import Rational, symbols, summation, oo

CANDIDATE = 3          # ★원문제 정답: ③ (절대 바꾸지 않음)

PARAMS = dict(
    a1=Rational(3),          # 첫째항
    r=Rational(1, 2),        # 공비
    choice_start=4,          # 보기 다섯 개(연속 정수)의 시작값
)

CIRCLED = ['①', '②', '③', '④', '⑤']


def value(prm):
    """무한등비급수의 합을 sympy summation 으로 실제 계산한다."""
    a1 = prm['a1']
    r = prm['r']
    if r == 0:
        raise ValueError('공비가 0이면 등비수열이 아닙니다.')
    if abs(r) >= 1:
        raise ValueError('|공비| >= 1 이면 무한등비급수가 수렴하지 않습니다.')
    n = symbols('n', positive=True, integer=True)
    term = a1 * r ** (n - 1)
    S = summation(term, (n, 1, oo))
    return S


def choices(prm):
    """값에서 유도된 보기 목록: choice_start 부터 시작하는 연속한 정수 5개."""
    v = value(prm)
    if not v.is_Integer:
        raise ValueError('무한급수의 합이 정수가 아니어서 보기를 구성할 수 없습니다.')
    start = prm['choice_start']
    return [start + i for i in range(5)]


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError('계산된 값이 보기 범위 안에 없습니다.')
    return ch.index(v) + 1  # 1~5 (①~⑤)


def statement(prm):
    a1 = prm['a1']
    r = prm['r']
    ch = choices(prm)
    opts = '    '.join(f'{CIRCLED[i]} {ch[i]}' for i in range(5))
    return (
        f"수열 \\{{a_n\\}}은 첫째항이 {a1}이고 공비가 {r}인 등비수열이다.\n"
        f"  \\sum_{{n=1}}^{{\\infty}} a_n의 값은? [3점]\n"
        f"  {opts}"
    )


# 원문제 보기가 그대로 재현되는지 고정
assert choices(PARAMS) == [4, 5, 6, 7, 8]

print(statement(PARAMS))
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
