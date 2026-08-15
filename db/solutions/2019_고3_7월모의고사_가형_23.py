"""2019 고3 7월모의고사 가형 23번 — 파라미터화 솔버.

원문제: sec θ = 10 일 때, tan²θ의 값을 구하시오.
  풀이: 피타고라스 항등식  sec²θ - tan²θ = 1  ⇒  tan²θ = sec²θ - 1 = 10² - 1 = 99.

파라미터화된 수학 구조:
  ① sec_val  : secθ 의 값 a (|a| > 1 이면 실수 범위에서 성립)
  ② power    : tanθ 의 차수 p (원문제는 p=2). 일반적으로
               tan^p θ = (sec²θ - 1)^(p/2)
  cosθ = 1/a, sin²θ = 1 - cos²θ 로부터 sympy 로 실제 대수 계산을 수행해
  tan²θ = sec²θ - 1 을 유도하고, 이를 p/2 제곱해 tan^p θ 를 구한다.
  a 와 p 를 각각 바꾸면 답이 서로 다른 값으로 바뀐다 (두 파라미터 모두 살아있음).
"""
import sympy as sp

CANDIDATE = 99  # ★원문제 정답 — 절대 변경 금지

PARAMS = dict(
    sec_val=10,   # secθ = a
    power=2,      # tan^power θ 를 구한다 (원문제는 2)
)


def solve(prm):
    a = sp.nsimplify(prm['sec_val'])
    p = sp.nsimplify(prm['power'])

    if sp.Abs(a) <= 1:
        raise ValueError('|secθ| > 1 이어야 cosθ=1/secθ 가 (-1,1) 범위의 실수 코사인이 된다')

    cos_t = 1 / a
    sin_t2 = sp.simplify(1 - cos_t**2)   # sin^2θ = 1 - cos^2θ
    tan_t2 = sp.simplify(sin_t2 / cos_t**2)  # tan^2θ = sec^2θ - 1 (sympy 로 실제 유도)

    if tan_t2 <= 0:
        raise ValueError('tan^2θ 가 양수가 아니어서 실수 거듭제곱을 정의할 수 없다')

    result = sp.simplify(tan_t2 ** (p / 2))
    return sp.nsimplify(result)


def statement(prm):
    a = prm['sec_val']
    p = prm['power']
    return f"sec θ = {a}일 때, tan^{{{p}}}θ의 값을 구하시오."


assert solve(PARAMS) == CANDIDATE
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
