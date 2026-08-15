import sympy as sp

# ── 원문제 정답: 5번 선택지(값 9) ──  ★절대 바꾸지 않는다
CANDIDATE = 5

# ── 문제를 정하는 파라미터 ──
#   c : f(x)=lim (( (x-c)/k )^{2n}-1)/((...)^{2n}+1) 에서 중심이동값 (원문제: x-1 → c=1)
#   p : x≠k 구간에서 g(x)=p*(x-k)^2 의 계수 (원문제: 계수 1 → p=1)
PARAMS = dict(c=1, p=1)


def _check_branch_values():
    """f(x) = lim_{n→∞} (t^{2n}-1)/(t^{2n}+1), t=(x-c)/k 가
    |t|<1→-1, |t|=1→0, |t|>1→1 이 됨을 실제 sympy 극한으로 검증한다."""
    n = sp.symbols('n', positive=True, integer=True)
    t = sp.symbols('t', positive=True)
    expr = (t ** (2 * n) - 1) / (t ** (2 * n) + 1)
    assert sp.limit(expr.subs(t, sp.Rational(1, 2)), n, sp.oo) == -1   # |t|<1
    assert sp.limit(expr.subs(t, 1), n, sp.oo) == 0                     # |t|=1
    assert sp.limit(expr.subs(t, 2), n, sp.oo) == 1                     # |t|>1


_check_branch_values()


def _f(xval, c, k):
    """f(x) = -1 (|x-c|<k), 0 (|x-c|=k), 1 (|x-c|>k)  (위에서 검증한 극한값)."""
    d = sp.Abs(xval - c)
    if d < k:
        return sp.Integer(-1)
    elif d == k:
        return sp.Integer(0)
    else:
        return sp.Integer(1)


def _find_k(c):
    """g가 x=k에서 연속이려면 lim_{x→k}(x-k)^2 = g(k) = f(f(k)) = 0 이어야 한다.
    k>c/2 라고 가정하면 |k-c|<k 이므로 f(k) = -1.
    이어서 f(-1)=0 이 되려면 |-1-c| = k 를 sympy 로 풀어 k를 구한다."""
    if c <= 0:
        raise ValueError('c는 양수여야 한다 (|x-c|<k 판별 구조상 필요)')
    ksym = sp.symbols('k', positive=True)
    sols = sp.solve(sp.Eq(sp.Abs(-1 - c), ksym), ksym)
    cands = [s for s in sols if s.is_real and s > sp.Rational(c, 2)]
    if not cands:
        raise ValueError('연속 조건을 만족하는 k가 없다')
    k = cands[0]
    if not (sp.Abs(k - c) < k):                 # f(k) = -1 가정 재검증
        raise ValueError('가정한 분기(k>c/2)가 성립하지 않는다')
    if _f(k, c, k) != -1:
        raise ValueError('f(k) != -1 이어서 이 분기로 풀 수 없다')
    if _f(_f(k, c, k), c, k) != 0:
        raise ValueError('연속조건 f(f(k))=0 을 만족하지 않는다')
    return k


def value(prm):
    """(g∘f)(k) 의 실제 수학적 값 = g(f(k)) = g(-1) = p*(-1-k)^2  (-1 ≠ k)."""
    c, p = prm['c'], prm['p']
    k = _find_k(c)
    fk = _f(k, c, k)                # = -1
    if fk == k:
        raise ValueError('g 정의 예외(-1 = k 인 경우 g가 정의된 분기가 달라진다)')
    return sp.nsimplify(p * (fk - k) ** 2)


def choices(prm):
    """실제 답(value)과, 자주 나오는 오답(부호·거듭제곱·계수 실수) 4개를
    함께 오름차순 정렬해 보기 5개를 만든다 — 값에서 유도한 보기."""
    c, p = prm['c'], prm['p']
    k = _find_k(c)
    v = value(prm)
    d1 = (k - 1) ** 2                 # f(k)를 -1이 아닌 +1로 착각(부호 오류)
    d2 = 2 * k - 1                    # 제곱을 잊고 선형으로 계산한 실수
    d3 = k ** 3 - k - 1               # k의 거듭제곱을 잘못 적용한 실수
    d4 = 5 * p ** 2 + 2 * k - 2       # p를 제곱으로 착각하는 등 계수 처리 실수
    vals = [sp.nsimplify(x) for x in (d1, d2, d3, d4, v)]
    if len(set(vals)) != 5:
        raise ValueError('보기 5개가 중복되어 객관식 문제로 성립하지 않는다')
    return tuple(sorted(vals))


def solve(prm):
    """value(prm)이 choices(prm) 중 몇 번째(1~5) 보기인지가 답(보기 번호)이다."""
    v = value(prm)
    ch = choices(prm)
    return ch.index(v) + 1


# 원문제(c=1, p=1)의 보기가 실제 문제의 ①1 ②3 ③5 ④7 ⑤9 와 일치하는지 고정 확인
assert choices(PARAMS) == (1, 3, 5, 7, 9)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
