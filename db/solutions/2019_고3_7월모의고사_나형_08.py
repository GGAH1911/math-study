"""
[원문제] 좌표평면에서 함수 y = 4/(x-3) + a 의 그래프가 직선 y = x 에 대하여
대칭일 때, 상수 a의 값은? (5지선다, 정답 ③ = 3)

[수학 구조 파라미터화]
함수 y = k/(x-h) + a 는 점근선 x=h, y=a 를 갖는 쌍곡선이고 그 중심은 (h, a) 이다.
이 쌍곡선이 직선 y = x + c 에 대해 대칭이려면(원문제는 c=0, 즉 y=x),
쌍곡선의 대각 대칭축 중 하나인 y - a = (x - h), 즉 y = x + (a - h) 가 바로
그 대칭축 y = x + c 와 일치해야 한다 → a - h = c → a = h + c.

이를 손으로 대입하지 않고, 원 풀이처럼 "f(f(x)-c) = x+c 가 항등식" 조건을
sympy 로 실제로 세우고 풀어서 a 를 구한다(계수 k 는 항등식이 성립하는 한
결과에 영향을 주지 않음 — 쌍곡선의 모양만 바꿀 뿐 중심 위치와는 무관하기 때문).

보기(다섯 개)는 원문제에서 "1,2,3,4,5" 로, 분자 상수 k 를 기준으로
[k-3, k-2, k-1, k, k+1] 형태로 만들어지는 구조로 두었다(k=4 → 1..5 재현).
정답 a=h+c 가 이 목록의 몇 번째인지가 실제 선택지 번호(=CANDIDATE)가 된다.
"""
from sympy import symbols, Eq, solve as sp_solve, together, simplify, fraction, Poly, expand

CANDIDATE = 3  # ★원문제 정답(선택지 번호 ③) — 절대 바꾸지 않음

# 문제를 정하는 값들
#  k : y=k/(x-h)+a 의 분자 상수 (0이면 쌍곡선이 성립하지 않음)   → 보기 목록을 결정
#  h : 점근선 x=h (분모의 이동량)                                → 답 a=h+c 에 직접 기여
#  c : 대칭축 직선 y=x+c 의 절편 (원문제는 c=0, 즉 "y=x")          → 답 a=h+c 에 직접 기여
PARAMS = dict(k=4, h=3, c=0)


def value(prm):
    """조건 f(f(x)-c) = x+c 가 모든 x에 대해 성립하도록 하는 상수 a를 sympy로 직접 구한다."""
    k, h, c = prm['k'], prm['h'], prm['c']
    if k == 0:
        raise ValueError("k=0 이면 y=k/(x-h)+a 가 쌍곡선이 아니어서 문제가 성립하지 않는다.")

    x, a = symbols('x a', real=True)

    def f(t):
        return k / (t - h) + a

    # (x0, f(x0)) 를 직선 y=x+c 에 대해 반사한 점이 다시 그래프 위에 있어야 한다는
    # 조건을 f(f(x)-c) = x+c 로 세운다(원 풀이의 f(f(x))=x 를 c=0 경우로 포함한다).
    expr = together(simplify(f(f(x) - c) - (x + c)))
    num, den = fraction(expr)
    poly = Poly(expand(num), x)

    # 이 유리식이 항등적으로 0 이려면 x 의 모든 계수가 0 이어야 한다.
    eqs = [Eq(coef, 0) for coef in poly.all_coeffs()]
    sols = sp_solve(eqs, a)
    if not sols:
        raise ValueError("모든 계수를 동시에 0으로 만드는 a 가 존재하지 않는다 — 대칭 조건 불성립.")

    vals = {s[0] if isinstance(s, tuple) else s for s in sols}
    if len(vals) != 1:
        raise ValueError(f"a 가 유일하게 정해지지 않는다: {sols}")
    return vals.pop()


def choices(prm):
    """분자 상수 k 로부터 유도되는 5개의 보기(정수 연속값)."""
    k = prm['k']
    return [k - 3, k - 2, k - 1, k, k + 1]


# 원문제 보기가 실제로 ①1 ②2 ③3 ④4 ⑤5 로 재현되는지 고정
assert tuple(choices(PARAMS)) == (1, 2, 3, 4, 5)


def solve(prm):
    """수학적 답 a 가 보기 목록에서 몇 번째(1-based)인지를 반환한다 = 선택지 번호."""
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f"a={v} 가 보기 목록 {ch} 안에 없다 — 이 조합은 문제로 성립하지 않는다.")
    return ch.index(v) + 1


def statement(prm):
    k, h, c = prm['k'], prm['h'], prm['c']
    hyperbola = f"y=\\frac{{{k}}}{{x-{h}}}+a" if h >= 0 else f"y=\\frac{{{k}}}{{x+{-h}}}+a"
    if c == 0:
        line = "y=x"
    elif c > 0:
        line = f"y=x+{c}"
    else:
        line = f"y=x-{-c}"
    marks = ['①', '②', '③', '④', '⑤']
    opts = ' '.join(f"{m}{v}" for m, v in zip(marks, choices(prm)))
    return (
        f"좌표평면에서 함수 {hyperbola} 의 그래프가 직선 {line} 에 대하여 "
        f"대칭일 때, 상수 a의 값은? {opts}"
    )


if __name__ == '__main__':
    print(statement(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
