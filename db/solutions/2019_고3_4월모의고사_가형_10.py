"""2019 고3 4월모의고사 가형 10번 — 파라미터 솔버 (수동 작성).
문제: f(x)=a cos(bx) 그래프(그림)에서 a,b 결정. g(x)=b sinx + a 의 최댓값. (b>0) (답 ② -1)
그림 판독: f(0)=a·cos0=a=-3 (그래프가 x=0서 최소 -3). 최소점이 x=0, π → 주기 π → b=2π/π=2.
구조: g(x)=b sinx + a, b>0 → 최댓값 = a + b = -3+2 = -1.
재생산: (a,b) 파라미터화.
"""
import sympy as sp


def gmax(a, b):
    x = sp.symbols('x')
    return sp.maximum(b * sp.sin(x) + a, x)      # b>0 → a+b


CANDIDATE = -1                                    # 보기 ② 의 값
assert gmax(-3, 2) == CANDIDATE, gmax(-3, 2)
print('VERIFY_PASS')
