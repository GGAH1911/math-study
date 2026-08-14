"""원문제(8번, [3점], choice):
  실수 전체의 집합에서 미분가능한 함수 f(x)가 모든 실수 x에 대하여
    f(5x-1) = e^{x^2-1}
  을 만족시킬 때, f'(4)의 값은?
  ① 1/10  ② 1/5  ③ 3/10  ④ 2/5  ⑤ 1/2   → 정답 ④ (=2/5)

--- 수학 구조 ---
f(a*x+b) = e^{x^2-c} 를 만족하는 f 에 대해 f'(d) 를 구한다.
  u = a*x+b 로 치환 → x = (u-b)/a
  f(u) = e^{((u-b)/a)^2 - c}
  f'(u) = e^{((u-b)/a)^2 - c} * 2*(u-b)/a^2
  f'(d) = e^{((d-b)/a)^2 - c} * 2*(d-b)/a^2

보기가 "깔끔한 분수" 5개로 떨어지는 원문제 유형이 되려면 지수부가 0이어야
하므로 c 는 독립적으로 아무 값이나 줄 수 없고 c = ((d-b)/a)^2 로 자동
결정된다 (원문제도 a=5,b=-1,d=4 → c=((4-(-1))/5)^2=1 로 이 조건을 만족).
→ 문제를 실제로 결정하는 손잡이는 a, b, d 세 개이고, a·d(또는 b) 를 바꾸면
   계수 2*(d-b)/a^2 자체가 바뀌어 정답(보기 번호)도 함께 바뀐다.
다만 a,b,d 는 "5지선다 격자(분모 2a) 위에 정확히 떨어져야 한다"는 정수
조건으로 서로 묶여 있어(자연수 해 조건과 같은 성격) 하나만 임의로 흔들면
보기 목록 밖으로 튀어나간다 → VARIANTS 로 실제로 성립하는 조합을 제시한다.
"""
import sympy as sp

CANDIDATE = 4  # 원문제 정답: ④ (보기 번호, [정답] 필드 값 그대로)

PARAMS = dict(a=5, b=-1, d=4)


def value(prm):
    """f'(d) 의 실제 값을 sympy 로 직접 미분해 구한다."""
    a = sp.nsimplify(prm['a'])
    b = sp.nsimplify(prm['b'])
    d = sp.nsimplify(prm['d'])
    if a == 0:
        raise ValueError('a=0 이면 u=a*x+b 치환이 R 위의 전단사가 되지 못한다')

    c = ((d - b) / a) ** 2  # 지수부가 0이 되도록 자동 결정되는 조건값

    x, u = sp.symbols('x u')
    x_of_u = (u - b) / a           # u = a*x+b 를 x 에 대해 풀기
    f_u = sp.exp(x_of_u ** 2 - c)  # f(u) = e^{((u-b)/a)^2 - c}

    # 조건 f(a*x+b) = e^{x^2-c} 재검증 (합성해서 원래 식으로 돌아오는지)
    check = sp.simplify(f_u.subs(u, a * x + b) - sp.exp(x ** 2 - c))
    if check != 0:
        raise ValueError('조건 f(a*x+b)=e^{x^2-c} 를 만족하지 않는다')

    fprime = sp.diff(f_u, u)
    v = sp.nsimplify(sp.simplify(fprime.subs(u, d)))
    if not getattr(v, 'is_number', False) or v.has(sp.zoo, sp.nan, sp.oo, sp.I):
        raise ValueError('유효한 값이 아니다')
    return v


def choices(prm):
    """값에서 유도한 5지선다 보기: 분모 2a 의 등차수열 n/(2a), n=1..5.
    value(prm) 이 이 격자 위의 정수 번째 항이어야 유효한 5지선다가 된다."""
    a = sp.nsimplify(prm['a'])
    denom = 2 * a
    v = value(prm)
    k = sp.nsimplify(v * denom)
    if k != sp.floor(k) or not (1 <= k <= 5):
        raise ValueError('이 파라미터 조합은 5지선다 격자에 정확히 맞지 않는다')
    return [sp.Rational(n, 1) / denom for n in range(1, 6)]


# 원문제 보기(① 1/10 ② 1/5 ③ 3/10 ④ 2/5 ⑤ 1/2)와 정확히 일치하는지 고정
assert choices(PARAMS) == [sp.Rational(1, 10), sp.Rational(1, 5),
                            sp.Rational(3, 10), sp.Rational(2, 5),
                            sp.Rational(1, 2)]


def solve(prm):
    """조건 → f'(d) 의 값 → 그 값이 위치한 보기 번호(1~5)."""
    ch = choices(prm)
    v = value(prm)
    return ch.index(v) + 1


def statement(prm):
    a, b, d = prm['a'], prm['b'], prm['d']
    c = sp.nsimplify(((sp.nsimplify(d) - sp.nsimplify(b)) / sp.nsimplify(a)) ** 2)
    ch = choices(prm)
    marks = ['①', '②', '③', '④', '⑤']
    opts = '  '.join(f'{m} {v}' for m, v in zip(marks, ch))
    sign = '+' if b >= 0 else '-'
    return (
        f"실수 전체의 집합에서 미분가능한 함수 f(x)가 모든 실수 x에 대하여 "
        f"f({a}x{sign}{abs(b)}) = e^(x^2-{c}) 을 만족시킬 때, f'({d}) 의 값은?\n"
        f"{opts}"
    )


# a,b,d 는 "5지선다 격자에 정확히 맞아야 한다"는 조건으로 서로 묶여 있어
# 한 파라미터만 임의로 흔들면 격자 밖으로 튀어나간다(예외 발생). 그래서
# 실제로 성립하는 조합을 VARIANTS 로 직접 제시한다. 둘 다 원문제(정답 4)와
# 다른 정답을 낸다.
VARIANTS = [
    dict(a=8, b=6, d=10),   # d-b=4  → f'(d)=1/8  → 보기 2번 (① ...⑤ 중 2/16=1/8)
    dict(a=4, b=0, d=5),    # d-b=5  → f'(d)=5/8  → 보기 5번
]

if __name__ == '__main__':
    print(statement(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
