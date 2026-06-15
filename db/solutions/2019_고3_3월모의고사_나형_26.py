"""2019 고3 3월모의고사 나형 26번 — 파라미터 솔버 (수동 작성).
문제: log_x(-x^2+4x+5) 가 정의되기 위한 모든 정수 x 의 합. (답 9)
구조: 로그 정의조건 — 밑 x>0, x≠1 ; 진수 -x^2+4x+5>0 ⇔ -1<x<5.
      교집합의 정수 x = {2,3,4} → 합 9.
재생산: 진수 2차식 계수 파라미터화.
"""


def solve(a, b, c, lo=-1000, hi=1000):
    res = [x for x in range(lo, hi + 1)
           if x > 0 and x != 1 and (a * x * x + b * x + c) > 0]
    return sum(res)


CANDIDATE = 9
assert solve(-1, 4, 5) == CANDIDATE, solve(-1, 4, 5)
print('VERIFY_PASS')
