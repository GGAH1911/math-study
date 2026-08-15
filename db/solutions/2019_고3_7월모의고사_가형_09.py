from sympy import symbols, exp, diff, solve as sp_solve, simplify, E, Rational

# ── 문제 구조 ──
# f(x) = e^{a x^3 + b x + c},  g = f^{-1} 일 때 g'(e) = 1 / f'(x0)  (단 f(x0)=e)
#
# 설계: c := 1 - a - b 로 고정해 x0=1 이 항상 f(x0)=e 의 (유일한) 실근이 되도록
#   만든다(원문제처럼 나머지 두 근은 허근). 그러면
#     f'(x0) = e * (3a + b)  →  g'(e) = 1 / ((3a+b) * e)
#   즉 a, b 가 "정답의 분모(k=3a+b)"를 결정하는 진짜 수학 파라미터다.
#
# 보기(5지선다)는 등차수열 anchor, anchor+step, ..., anchor+4*step 의 각 항을
#   분모로 하는 값들이고, 정답 번호는 k 가 그 수열에서 몇 번째 항인지로 정해진다.
#   원문제는 anchor=1, step=2 → 분모 1,3,5,7,9 이고 k=5 는 3번째 → 정답 ③.
#   anchor·step 을 바꾸면 같은 k 라도 보기 안에서의 자리가 달라져 정답 번호가 바뀌고,
#   a·b 를 바꾸면 k 자체(따라서 g'(e)의 값)가 바뀐다.

CANDIDATE = 3          # ★원문제 정답: ③

PARAMS = dict(a=1, b=2, anchor=1, step=2)


def _core(prm):
    """a,b,anchor,step → (정답 분모 k, g'(e) 의 값, anchor, step)."""
    a, b = prm['a'], prm['b']
    anchor, step = prm['anchor'], prm['step']
    x = symbols('x', real=True)
    c = 1 - a - b                       # a+b+c = 1  →  x=1 이 f(x)=e 의 해가 되도록 고정
    inner = a * x**3 + b * x + c
    f = exp(inner)
    f_prime = diff(f, x)

    roots = sp_solve(inner - 1, x)       # f(x0) = e  ⇔  inner(x0) = 1
    real_roots = [r for r in roots if r.is_real]
    if len(real_roots) != 1:
        raise ValueError(f'실근이 정확히 1개가 아님: {real_roots}')
    x0 = real_roots[0]
    if simplify(x0 - 1) != 0:
        raise ValueError('설계 조건(x0=1) 위반')

    fp_over_e = simplify(f_prime.subs(x, x0) / E)   # k = f'(x0)/e
    if not fp_over_e.is_integer:
        raise ValueError(f'분모 계수가 정수가 아님: {fp_over_e}')
    k = int(fp_over_e)
    if k == 0:
        raise ValueError('g\'(e) 의 분모가 0')

    g_prime_e = Rational(1, 1) / (k * E)
    return k, g_prime_e, anchor, step


def _denoms(prm):
    k, _, anchor, step = _core(prm)
    denoms = [anchor + i * step for i in range(5)]
    if len(set(denoms)) != 5 or any(d == 0 for d in denoms):
        raise ValueError(f'보기 분모가 유효하지 않음: {denoms}')
    return k, denoms


def value(prm):
    """수학적 답: g'(e)."""
    _, v, _, _ = _core(prm)
    return v


def choices(prm):
    """5지선다 보기 목록(정답 분모 k를 등차수열 위에 배치해 유도)."""
    _, denoms = _denoms(prm)
    return [Rational(1, 1) / (d * E) for d in denoms]


def solve(prm):
    """보기 번호(1~5)."""
    k, denoms = _denoms(prm)
    if k not in denoms:
        raise ValueError(f'정답 k={k} 이 보기 목록 {denoms} 안에 없음')
    return denoms.index(k) + 1


def statement(prm):
    a, b = prm['a'], prm['b']
    c = 1 - a - b
    c_str = f'+ {c}' if c >= 0 else f'- {-c}'
    return (f"함수 f(x)=e^(({a})x^3+({b})x{c_str})의 역함수를 g(x)라 할 때, "
            f"g'(e)의 값은?")


# 원문제 보기(①1/e ②1/3e ③1/5e ④1/7e ⑤1/9e) 재현 확인
_expected = [Rational(1, 1) / (d * E) for d in (1, 3, 5, 7, 9)]
_got = choices(PARAMS)
assert all(simplify(_got[i] - _expected[i]) == 0 for i in range(5)), _got

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
