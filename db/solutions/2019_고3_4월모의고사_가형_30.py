"""2019 고3 4월모의고사 가형 30번 — 파라미터화 솔버.

원문제: 삼차함수 f(x)=x^3+ax^2+bx (a,b 정수) 에 대해
  g(x)=e^{f(x)}-f(x) 가 x=α, x=-1, x=β (α<-1<β) 에서만 극값을 갖고,
  y=|g(x)-g(α)| 가 미분가능하지 않은 점의 개수가 2일 때 {f(-1)}² 의 최댓값을 구하라. (답 9)

수학 구조
  · g=G(f), G(t)=e^t-t 는 t=0 에서 최소이므로 G'(t)=e^t-1 은 t 와 부호가 같다.
    ⇒ sign g'(x) = sign f'(x) · sign f(x).
  · g 의 극값 후보 = {f'(x)=0} ∪ {f(x)=0 인 단순근} 이고, 그중 실제로 좌우 부호가
    바뀌는 점만 극값이다. f',f 의 실근은 sympy Poly.real_roots() 로 정확히 구한다
    (수치 근사가 아니라 스튀름열 기반의 엄밀한 실근 분리).
  · y=|g(x)-g(ref)| 가 미분불가능한 점 = g(x)=g(ref) 를 g'≠0 으로 "횡단"하는 점의 개수
    (극값점에서의 접촉은 짝수차 접촉이라 미분가능).

파라미터화 (원문제의 "-1"과 "2개"라는 두 상수를 구조 변수로 분리)
  · m       : g가 갖는 가운데 극값의 위치(원문제의 "-1"). f(m) 의 제곱이 구하려는 값.
  · k       : y=|g(x)-g(ref)| 가 미분불가능한 점의 개수 조건(원문제의 "2").
  · ref_idx : |g(x)-g(ref)| 의 기준점 ref = 극값 3개 {α,m,β} 중 몇 번째인가
              (0=α, 1=m, 2=β). 원문제는 ref_idx=0 (g(α) 기준).
  · rng     : 정수 (a,b) 탐색 구간의 절댓값 상한.
  m,k 는 서로 묶여 있다 — g 의 극값 배치상, m 이 정해지면 ref_idx 위치에서 가능한
  미분불가 점 개수 k 는 사실상 정해진다(예: m<0 이면 ref=α 에서 k=2, m>0 이면 k=0).
  그래서 임의로 하나만 바꾸면 해가 사라지므로 VARIANTS 로 성립하는 (m,k) 조합을 제시한다.
"""
import sympy as sp
import numpy as np

x = sp.symbols('x', real=True)


def _extrema_and_funcs(a, b):
    """f(x)=x^3+ax^2+bx 에 대해 g(x)=e^{f(x)}-f(x) 의 실제 극값점들을 정확히 구한다."""
    f_expr = x ** 3 + a * x ** 2 + b * x
    fp_expr = sp.diff(f_expr, x)
    fp_roots = [complex(r.evalf(25)).real for r in sp.Poly(fp_expr, x).real_roots()]
    f_roots = [complex(r.evalf(25)).real for r in sp.Poly(f_expr, x).real_roots()]
    cand = sorted({round(c, 7) for c in fp_roots + f_roots})

    def fx(v):
        return v ** 3 + a * v * v + b * v

    def fpx(v):
        return 3 * v * v + 2 * a * v + b

    def sgn(v):
        p, q = fpx(v), fx(v)
        sp_ = 0 if abs(p) < 1e-9 else (1 if p > 0 else -1)
        sq_ = 0 if abs(q) < 1e-9 else (1 if q > 0 else -1)
        return sp_ * sq_

    ext = []
    for c in cand:
        s1, s2 = sgn(c - 1e-5), sgn(c + 1e-5)
        if s1 != 0 and s2 != 0 and s1 != s2:          # g'(x) 부호가 실제로 바뀌는 점 = 극값
            ext.append(c)
    return sorted({round(e, 6) for e in ext}), fx, fpx


def _nondiff_count(fx, fpx, ref, n=200_000, pad=10):
    """y=|g(x)-g(ref)| 가 미분불가능한 점(=g'≠0 으로 횡단하는 g(x)=g(ref) 의 해) 개수."""
    fref = fx(ref)
    gref = np.exp(np.clip(fref, -50, 50)) - fref
    xs = np.linspace(ref - pad, ref + pad, n)
    g = np.exp(np.clip(fx(xs), -50, 50)) - fx(xs)
    s = np.sign(g - gref)
    nd = 0
    for i in np.where(s[:-1] * s[1:] < 0)[0]:
        xm = xs[i]
        if abs(fpx(xm)) > 1e-6 and abs(fx(xm)) > 1e-6:      # g'(xm) = f'·(e^f-1) ≠ 0 (횡단)
            nd += 1
    return nd


def solve(prm):
    """정수 (a,b) 를 전수 탐색해 조건을 만족하는 것 중 {f(m)}² 의 최댓값을 구한다."""
    m, k, ref_idx, rng = prm['m'], prm['k'], prm['ref_idx'], prm['rng']
    best = None
    for a in range(-rng, rng + 1):
        for b in range(-rng, rng + 1):
            ext, fx, fpx = _extrema_and_funcs(a, b)
            if len(ext) != 3:                                   # 극값이 정확히 3개(α,m,β)
                continue
            if abs(ext[1] - m) > 1e-4 or not (ext[0] < m < ext[2]):
                continue
            ref = ext[ref_idx]
            if _nondiff_count(fx, fpx, ref) != k:
                continue
            val = fx(m) ** 2
            if best is None or val > best:
                best = val
    if best is None:
        raise ValueError(f'조건을 만족하는 정수 (a,b) 가 없음: prm={prm}')
    return sp.Integer(round(best))


_REF_NAME = {0: 'α', 1: '가운데 극값점', 2: 'β'}


def statement(prm):
    m, k, ref_idx = prm['m'], prm['k'], prm['ref_idx']
    ref = _REF_NAME[ref_idx]
    return (
        f"삼차함수 f(x)=x^3+ax^2+bx (a, b는 정수)에 대하여 함수 g(x)=e^{{f(x)}}-f(x)는 "
        f"x=α, x={m}, x=β (α<{m}<β)에서만 극값을 갖는다. 함수 y=|g(x)-g({ref})|가 "
        f"미분가능하지 않은 점의 개수가 {k}일 때, {{f({m})}}^2의 최댓값을 구하시오."
    )


CANDIDATE = 9

# m,k 가 서로 묶여 있어(가운데 극값 위치가 정해지면 기준점에서의 미분불가 점 개수도
# 사실상 정해짐) 하나만 독립적으로 흔들 수 없다 — 성립하는 (m,k) 조합을 직접 제시한다.
VARIANTS = [
    dict(m=-1, k=2, ref_idx=0, rng=15),   # 원문제 그대로 → 9
    dict(m=1, k=0, ref_idx=0, rng=15),    # 가운데 극값이 x=1 → 9 (부호 대칭)
    dict(m=-2, k=2, ref_idx=0, rng=20),   # 가운데 극값이 x=-2 → 144
    dict(m=2, k=0, ref_idx=0, rng=20),    # 가운데 극값이 x=2 → 144
]

PARAMS = VARIANTS[0]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
