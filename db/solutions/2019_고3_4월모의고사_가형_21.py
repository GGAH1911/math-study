"""2019 고3 4월모의고사 가형 21번 — 파라미터 솔버 (수동 작성).
문제: 자연수 n. 열린구간 (3n-3, 3n) 에서
      f(x)=(2x-3n)sin2x-(2x^2-6nx+4n^2-1)cos2x 가 극대/극소가 되는 모든 α의 합을 a_n.
      cos(a_m)=0 인 최소 자연수 m 을 l 이라 할 때 Σ_{k=1}^{l+2} a_k. (답 ① 7+45π/2)
구조: f'(x)=4 sin2x (x-n)(x-2n) (곱·합 미분 후 정리). 극점 = (3n-3,3n) 내 f'의 부호변화 영점.
      영점: x=n, x=2n (구간 내부일 때), x=kπ/2 (sin2x=0). 모두 단순근 → 전부 극점.
      a_1=3+π/2, a_2=4+5π/2, a_3=9π/2 → cos(9π/2)=0 → l=3.
      Σ_{k=1}^{5}=7+(1+5+9+13+17)π/2 = 7+45π/2.
재생산: 계수(3n, 4n^2-1 …)·구간을 n 으로 파라미터화.
"""
import math
import sympy as sp
from sympy import pi, Rational


def f_prime(x, n):
    # 원식 미분의 닫힌형 (검증용): 4 sin2x (x-n)(x-2n)
    return 4 * sp.sin(2 * x) * (x - n) * (x - 2 * n)


def a(n):
    lo, hi = 3 * n - 3, 3 * n
    zeros = set()
    for r in (n, 2 * n):                              # 정수근, 열린구간 내부만
        if lo < r < hi:
            zeros.add(sp.Integer(r))
    klo = math.floor(lo * 2 / math.pi) - 1            # sin2x=0 → x=kπ/2
    khi = math.ceil(hi * 2 / math.pi) + 1
    for k in range(klo, khi + 1):
        x = Rational(k, 2) * pi
        if lo < float(x) < hi:
            zeros.add(x)
    return sp.nsimplify(sum(zeros))


def solve():
    m = 1
    while sp.simplify(sp.cos(a(m))) != 0:             # cos(a_m)=0 인 최소 자연수
        m += 1
        if m > 50:
            raise RuntimeError('no l found')
    l = m
    return sp.simplify(sum(a(k) for k in range(1, l + 2 + 1)))   # Σ_{k=1}^{l+2}


# 미분 닫힌형 자가검증: 원식 f 를 직접 미분한 것과 4 sin2x(x-n)(x-2n) 가 같은지
_x, _n = sp.symbols('x n')
_f = (2 * _x - 3 * _n) * sp.sin(2 * _x) - (2 * _x ** 2 - 6 * _n * _x + 4 * _n ** 2 - 1) * sp.cos(2 * _x)
assert sp.simplify(sp.diff(_f, _x) - f_prime(_x, _n)) == 0, 'f 미분 불일치'

CANDIDATE = 7 + Rational(45, 2) * pi                  # 보기 ①
assert sp.simplify(solve() - CANDIDATE) == 0, solve()
print('VERIFY_PASS')
