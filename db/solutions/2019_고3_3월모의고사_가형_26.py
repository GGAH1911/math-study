"""2019 고3 3월모의고사 가형 26번 — 파라미터 솔버 (수동 작성).
문제: 0≤x≤π, n≥2 자연수. y=sin x 와 y=sin(nx) 의 교점 개수를 a_n.
      a_3 + a_5 의 값. (답 9)
구조: sin(nx)=sin(x) ⟺ nx = x + 2kπ  또는  nx = π - x + 2kπ.
      (n-1)x = 2kπ → x = 2kπ/(n-1) ;  (n+1)x = (2k+1)π → x = (2k+1)π/(n+1).
      [0,π] 안의 서로 다른 x (= x/π ∈ [0,1] 유리수) 개수가 a_n.
      a_3 = #{0, 1/4, 3/4, 1} = 4 ;  a_5 = #{0, 1/6, 1/2, 5/6, 1} = 5 → 합 9.
재생산: (m, n) 등 인덱스 바꾸면 동종 문제 무한 생성.
"""
import sympy as sp


def a(n):
    sols = set()                       # x/π 값(유리수)으로 [0,1] 안의 교점
    if n != 1:                         # nx = x + 2kπ
        k = 0
        while sp.Rational(2 * k, n - 1) <= 1:
            sols.add(sp.Rational(2 * k, n - 1)); k += 1
    k = 0                              # nx = π - x + 2kπ
    while sp.Rational(2 * k + 1, n + 1) <= 1:
        sols.add(sp.Rational(2 * k + 1, n + 1)); k += 1
    return len(sols)


CANDIDATE = 9
assert a(3) + a(5) == CANDIDATE, (a(3), a(5))
print('VERIFY_PASS')
