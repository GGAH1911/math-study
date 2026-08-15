"""
수능형 로그부등식 문제의 파라미터화 솔버.

원문제: log_3(x-3) + log_3(x+3) <= 3 을 만족시키는 모든 정수 x의 값의 합은?
        (① 15 ② 17 ③ 19 ④ 21 ⑤ 23, 정답 ①)

구조 분석
  log_b(x-a) + log_b(x+a) <= c
  → 정의역: x-a>0, x+a>0 중 더 강한 조건인 x > a
  → 두 로그의 합을 곱으로: (x-a)(x+a) <= b^c, 즉 x^2 <= a^2 + b^c
  → x <= U := sqrt(a^2+b^c)
  → 정수해의 합 S0 = sum_{k=a+1}^{floor(U)} k

파라미터로 뽑은 값: a(이동 상수), b(로그의 밑), c(부등식 우변). 세 값 모두
sympy 로 실제 부등식을 풀어 S0 을 구하는 데 직접 쓰이므로, 값을 바꾸면 정답
(그리고 아래에서 만드는 보기 번호)이 실제로 달라진다.

보기(선택지) 생성 구조
  원문제 보기 15,17,19,21,23 은 정답 S0=15 에 "흔한 실수" 오프셋 4개를 더한
  값들이다.
    g1 = 14-4a  : 정의역 경계 x=a 처리 관련 실수 계열 (a=3 → 2)
    g2 = 16-4b  : 로그의 밑 b 관련 계산 실수 계열   (b=3 → 4)
    g3 = 18-4c  : 부등식 우변 c 관련 계산 실수 계열  (c=3 → 6)
    g4 = 8      : 고정 오차 (항상 정답보다 커 보이는 매력적 오답)
  {S0, S0+g1, S0+g2, S0+g3, S0+g4} 를 오름차순 정렬했을 때 S0 이 몇 번째에
  오는지가 정답 보기 번호다. a,b,c 를 키우면 g1,g2,g3 가 음수로 뒤집히며
  (예: a=4 → g1=-2) 정렬 순위 자체가 바뀐다 — 즉 a,b,c 는 장식이 아니라
  실제로 정답(보기 번호)을 바꾸는 파라미터다.
"""
import sympy as sp

CANDIDATE = 1  # 원문제 정답: ① (수학적 값은 15)

PARAMS = dict(
    a=3,   # x-a, x+a 의 이동 상수 (원문제: x-3, x+3)
    b=3,   # 로그의 밑
    c=3,   # 부등식 우변 (두 로그의 합 <= c)
)


def _upper_bound(a, b, c):
    """sympy 로 log_b(x-a)+log_b(x+a) <= c 를 실제로 풀어 정수 상한 U를 구한다."""
    x = sp.symbols('x', positive=True)
    ineq = sp.Le((x - a) * (x + a), b ** c)
    sol = sp.solve_univariate_inequality(
        ineq, x, relational=False, domain=sp.Interval.open(a, sp.oo)
    )
    if sol is sp.EmptySet:
        raise ValueError('정의역 안에 해가 없음')
    U = sp.floor(sol.sup)
    if U <= a:
        raise ValueError('정수해가 존재하지 않음')
    return U


def value(prm):
    """수학적 정답: 부등식을 만족하는 모든 정수 x의 합을 sympy 로 계산."""
    a, b, c = sp.Integer(prm['a']), sp.Integer(prm['b']), sp.Integer(prm['c'])
    U = _upper_bound(a, b, c)
    k = sp.symbols('k', integer=True)
    return sp.summation(k, (k, a + 1, U))


def choices(prm):
    """정답 + '흔한 실수' 오답 4개를 오름차순 정렬해 5지선다 보기를 만든다."""
    a, b, c = sp.Integer(prm['a']), sp.Integer(prm['b']), sp.Integer(prm['c'])
    S0 = value(prm)
    gaps = [14 - 4 * a, 16 - 4 * b, 18 - 4 * c, sp.Integer(8)]
    raw = [S0] + [S0 + g for g in gaps]
    uniq = sorted(set(raw))
    if len(uniq) != 5:
        raise ValueError('보기 값이 서로 겹쳐 문제가 성립하지 않음')
    return tuple(uniq)


def solve(prm):
    """정답이 보기 중 몇 번째(①=1, ②=2, ...)인지를 반환."""
    opts = choices(prm)
    S0 = value(prm)
    return opts.index(S0) + 1


def statement(prm):
    a, b, c = prm['a'], prm['b'], prm['c']
    opts = choices(prm)
    circled = ['①', '②', '③', '④', '⑤']
    opt_str = ' '.join(f'{circled[i]} {v}' for i, v in enumerate(opts))
    return (
        f'부등식 log_{b}(x-{a}) + log_{b}(x+{a}) \\le {c} 를 만족시키는 모든 '
        f'정수 x의 값의 합은?\n{opt_str}'
    )


# 원문제 보기(15,17,19,21,23)를 정확히 재현하는지 고정
assert choices(PARAMS) == (15, 17, 19, 21, 23)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
