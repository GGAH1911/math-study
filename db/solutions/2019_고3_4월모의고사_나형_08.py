"""
[원문제] 함수 f(x)가 lim_{x->1} (x-1)f(x)=3 을 만족시킬 때,
         lim_{x->1} (x^2-1)f(x) 의 값은? (5지선다)

[수학 구조]
  lim_{x->c} (x-c)f(x) = A 가 주어졌을 때
  lim_{x->c} (x^2-c^2)f(x) = lim_{x->c} (x-c)f(x) * (x+c)
                            = A * lim_{x->c} (x+c)   (극한의 곱의 성질)
                            = A * 2c
  즉 정답은 '극한이 걸리는 점 c' 와 '극한값 A' 두 파라미터의 곱 2cA 로 결정된다.
  원문제는 c=1, A=3 인 경우이며, 이때 정답 값은 2*1*3=6, 그 값이 보기
  ①5 ②6 ③7 ④8 ⑤9 중 두 번째(②)에 위치해 CANDIDATE=2 가 된다.

[보기 구성]
  오답 4개는 '곱셈 성질을 잘못 적용한 전형적인 실수'들을 c, A 로 표현한 것이다.
  c=1, A=3 을 넣으면 정확히 원문제의 보기 {5,6,7,8,9} 가 재현된다.
  c 또는 A 를 바꾸면 정답 값뿐 아니라 정답이 보기 중 몇 번째에 오는지(=solve 의 반환값)
  까지 실제로 달라진다(아래 VERIFY 로 직접 확인).
"""
import sympy as sp

x = sp.symbols('x')


def value(prm):
    """수학적 답: lim_{x->c} (x^2-c^2)f(x) = A * lim_{x->c}(x+c) = 2cA.

    lim_{x->c}(x+c) 부분은 sympy.limit 으로 실제 계산한다(단순 대입이 아님).
    """
    c = sp.nsimplify(prm['c'])
    A = sp.nsimplify(prm['A'])
    factor = sp.limit(x + c, x, c)   # = 2c, 인수분해로 나온 (x+c) 항의 극한
    return sp.nsimplify(A * factor)


def distractors(prm):
    """전형적인 오답 4개(곱의 극한 법칙을 잘못 적용했을 때 나오는 값들)."""
    c = sp.nsimplify(prm['c'])
    A = sp.nsimplify(prm['A'])
    return [
        2 * (A + c),      # 오답1: (x-c)f(x)*(x+c) 를 곱이 아닌 (A+c)에 2배로 착각
        3 * A,             # 오답2: (x^2-c^2)을 (x-c)(x+c) 대신 3(x-c)로 착각해 3A로 계산
        2 * c + A + 2,     # 오답3: 상수항 처리 실수로 2c+A에 2를 더함
        5 * c + A - 3,     # 오답4: 인수분해 계수를 잘못 잡아 5c+A-3으로 계산
    ]


def choices(prm):
    """보기 목록(값에서 유도). 5개가 모두 서로 다른 양수여야 문제로 성립한다."""
    v = value(prm)
    vals = [v] + distractors(prm)
    if len(set(vals)) != 5:
        raise ValueError('보기 값이 중복되어 문제로 성립하지 않음')
    if any((not getattr(val, 'is_number', False)) or val <= 0 for val in vals):
        raise ValueError('보기 값이 유효하지 않음(0 이하 또는 비수)')
    return sorted(vals)


def solve(prm):
    """정답의 보기 번호(1-based, ①=1)를 반환한다."""
    v = value(prm)
    ch = choices(prm)
    return ch.index(v) + 1


def statement(prm):
    c = prm['c']
    A = prm['A']
    c2 = sp.nsimplify(prm['c']) ** 2
    ch = choices(prm)
    circled = ['①', '②', '③', '④', '⑤']
    opts = ' '.join(f'{circled[i]}{ch[i]}' for i in range(5))
    return (
        f"함수 f(x)가 lim_{{x->{c}}} (x-{c})f(x)={A}을 만족시킬 때, "
        f"lim_{{x->{c}}} (x^2-{c2})f(x)의 값은?\n{opts}"
    )


CANDIDATE = 2   # ★원문제 정답(보기 번호) — 절대 바꾸지 않음
PARAMS = dict(c=1, A=3)

# 원문제 보기 {5,6,7,8,9} 가 그대로 재현되는지 고정
assert choices(PARAMS) == [5, 6, 7, 8, 9], f'보기 재현 실패: {choices(PARAMS)}'

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
