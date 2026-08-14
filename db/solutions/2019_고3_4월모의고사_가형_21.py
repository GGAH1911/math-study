"""2019 고3 4월모의고사 가형 21번 — 파라미터 솔버.

원문제: 자연수 n. 열린구간 (3n-3, 3n) 에서
      f(x)=(2x-3n)sin2x-(2x^2-6nx+4n^2-1)cos2x 가 극대/극소가 되는 모든 α의 합을 a_n.
      cos(a_m)=0 인 최소 자연수 m 을 l 이라 할 때 Σ_{k=1}^{l+2} a_k. (답 ① 7+45π/2)

★수학 구조 (파라미터화의 근거)
  f(x) = (2x - s)sin2x - (2x^2 + Bx + C)cos2x 를 미분하면
      f'(x) = 2sin2x + (2x-s)·2cos2x - (4x+B)cos2x + (2x^2+Bx+C)·2sin2x
  이고, cos2x 계수가 항등적으로 0 이 되도록(=sin2x 배수만 남도록) s,B,C 를 고르면
      f'(x) = [2 + 2(2x^2+Bx+C)]·sin2x
  가 되는데, 이를 4sin2x·(x-r1·n)(x-r2·n) (두 근 r1·n, r2·n) 꼴로 맞추면
      s = n(r1+r2),  B = -2s,  C = 2·r1·r2·n^2 - 1
  로 완전히 정해진다(아래 assert 로 항상 재검증). 원문제는 r1=1, r2=2 인 경우
  (s=3n, B=-6n, C=4n^2-1) 이다.
  즉 문제를 결정하는 것은
    - r1, r2 : f'(x)=0 의 두 다항근이 n 의 몇 배인가 (근이 구간 안에 드느냐가 답의 핵심)
    - iw     : 열린구간 (iw·n-iw, iw·n) 의 폭
  이 세 값이며, 이들을 바꾸면 각 a_n 에 들어가는 항(다항근 포함 여부·kπ/2 들의 개수)이
  달라져 답 자체가 바뀐다.
"""
import math
import sympy as sp
from sympy import pi, Rational


def build_f(x, n, r1, r2):
    # 도함수가 4 sin2x (x-r1 n)(x-r2 n) 이 되도록 역산한 f(x)
    s = n * (r1 + r2)
    B = -2 * s
    C = 2 * r1 * r2 * n ** 2 - 1
    return (2 * x - s) * sp.sin(2 * x) - (2 * x ** 2 + B * x + C) * sp.cos(2 * x)


def f_prime_closed(x, n, r1, r2):
    return 4 * sp.sin(2 * x) * (x - r1 * n) * (x - r2 * n)


def compute_a(n, r1, r2, iw):
    """구간 (iw*n-iw, iw*n) 안에서 f' 의 부호변화 영점들의 합 = a_n."""
    lo, hi = iw * n - iw, iw * n
    if lo >= hi:
        raise ValueError(f'구간이 비어있음: n={n}, iw={iw}')
    zeros = set()
    root1, root2 = sp.nsimplify(r1) * n, sp.nsimplify(r2) * n
    if root1 == root2:
        raise ValueError('r1, r2 는 서로 달라야 함 (다항근이 겹치면 부호변화가 사라짐)')
    for r in (root1, root2):                          # 다항식 인수의 근, 구간 내부일 때만
        if lo < r < hi:
            zeros.add(sp.nsimplify(r))
    klo = math.floor(lo * 2 / math.pi) - 1             # sin2x=0 → x=kπ/2
    khi = math.ceil(hi * 2 / math.pi) + 1
    for k in range(klo, khi + 1):
        xk = Rational(k, 2) * pi
        if lo < float(xk) < hi:
            zeros.add(xk)
    if not zeros:
        raise ValueError(f'n={n}: 구간 안에 극점이 없음')
    return sp.nsimplify(sum(zeros))


def solve(prm):
    r1, r2, iw = prm['r1'], prm['r2'], prm['iw']
    mmax = prm.get('mmax', 50)
    m = 1
    while sp.simplify(sp.cos(compute_a(m, r1, r2, iw))) != 0:   # cos(a_m)=0 인 최소 자연수 m
        m += 1
        if m > mmax:
            raise RuntimeError(f'l 을 mmax={mmax} 이내에서 찾지 못함 (r1={r1},r2={r2},iw={iw})')
    l = m
    return sp.simplify(sum(compute_a(k, r1, r2, iw) for k in range(1, l + 2 + 1)))


def statement(prm):
    r1, r2, iw = prm['r1'], prm['r2'], prm['iw']
    s = sp.Symbol('n') * (r1 + r2)
    B = -2 * s
    C = 2 * r1 * r2 * sp.Symbol('n') ** 2 - 1
    return (
        f'자연수 n에 대하여 열린 구간 ({iw}n-{iw}, {iw}n)에서 함수 '
        f'f(x)=(2x-{s})sin2x-(2x^2+({B})x+{C})cos2x 가 x=α에서 극대 또는 극소가 되는 '
        f'모든 α의 값의 합을 a_n이라 하자. cos a_m = 0이 되도록 하는 자연수 m의 최솟값을 l이라 할 때, '
        f'Σ_{{k=1}}^{{l+2}} a_k의 값은?'
    )


# 도함수 닫힌형 자가검증: 일반 r1,r2 에 대해서도 항등식이 성립하는지 심볼릭으로 재확인
_x, _n, _r1, _r2 = sp.symbols('x n r1 r2')
_f = build_f(_x, _n, _r1, _r2)
assert sp.simplify(sp.diff(_f, _x) - f_prime_closed(_x, _n, _r1, _r2)) == 0, 'f 미분 불일치'

PARAMS = dict(r1=1, r2=2, iw=3)                        # 원문제: (x-n)(x-2n), 구간폭 3
CANDIDATE = 7 + Rational(45, 2) * pi                    # 보기 ① 7+45π/2

if __name__ == '__main__':
    print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
