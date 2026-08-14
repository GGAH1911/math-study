from sympy import Rational, symbols, Eq, simplify
from sympy import solve as sympy_solve

CANDIDATE = 21  # ★ 원문제의 정답. 절대 바꾸지 않는다.

# 문제의 수학 구조
#   f(x) = (base_num/base_den)^(k*x - a)   (구간 [p, q])
#   이 구간에서 f의 최댓값이 M으로 주어질 때, a를 구하고
#   그때의 최솟값 m을 구해 a*m 의 값을 계산한다.
#
# 파라미터로 뽑아낸 구조:
#   base_num/base_den : 지수함수의 밑 b (0<b, b≠1). b<1이면 감소, b>1이면 증가하는
#                        지수함수가 되어 최댓값/최솟값이 어느 끝점에서 나오는지가 갈린다.
#   k                  : 지수 안의 x 계수. 부호에 따라 지수 kx-a가 x에 대해
#                        증가/감소하는지가 갈리고, 이는 b와 결합해 f(x)의 단조성(증가/감소)을 결정한다.
#   p, q               : 정의역 닫힌구간 [p, q] (p<q)의 양 끝점.
#   M                  : 최댓값으로 주어지는 값. 이 값으로부터 a가 결정된다.
PARAMS = dict(base_num=1, base_den=3, k=2, p=2, q=3, M=27)


def _monotonic_increasing(b, k):
    """f(x) = b^(k x - a) 가 x에 대해 증가함수인지 여부.
    b>1이면 지수함수 자체가 증가, b<1이면 감소.
    kx-a는 k>0이면 x에 대해 증가, k<0이면 감소.
    두 성질의 배타적결합(같은 방향이면 f는 x에 대해 증가)."""
    return (b > 1) == (k > 0)


def solve(prm):
    base_num = prm['base_num']
    base_den = prm['base_den']
    k = prm['k']
    p = prm['p']
    q = prm['q']
    M = Rational(prm['M'])

    if base_num <= 0 or base_den <= 0:
        raise ValueError('밑은 양수여야 합니다.')
    b = Rational(base_num, base_den)
    if b == 1:
        raise ValueError('밑이 1이면 상수함수라 최댓값/최솟값 문제가 성립하지 않습니다.')
    if k == 0:
        raise ValueError('k가 0이면 상수함수가 되어 문제가 성립하지 않습니다.')
    if not (p < q):
        raise ValueError('구간은 p < q 이어야 합니다.')

    increasing = _monotonic_increasing(b, k)
    x_max, x_min = (q, p) if increasing else (p, q)  # f가 최대/최소가 되는 x값

    a = symbols('a')
    # 최댓값 조건: f(x_max) = M  →  b^(k*x_max - a) = M 을 a에 대해 실제로 sympy로 푼다.
    eq = Eq(b ** (k * x_max - a), M)
    sols = sympy_solve(eq, a)
    real_sols = [s for s in sols if s.is_real]
    if not real_sols:
        raise ValueError('주어진 조건을 만족하는 실수 a가 존재하지 않습니다.')
    a_val = real_sols[0]

    m = b ** (k * x_min - a_val)  # 최솟값
    answer = simplify(a_val * m)
    if not answer.is_rational:
        raise ValueError('a×m 값이 유리수로 정리되지 않습니다.')
    return answer


def statement(prm):
    base_num = prm['base_num']
    base_den = prm['base_den']
    k = prm['k']
    p = prm['p']
    q = prm['q']
    M = prm['M']
    return (
        f"닫힌 구간 [{p}, {q}]에서 함수 "
        f"f(x)=\\left(\\frac{{{base_num}}}{{{base_den}}}\\right)^{{{k}x-a}}의 "
        f"최댓값은 {M}, 최솟값은 m이다. a\\times m의 값을 구하시오. (단, a는 상수이다.)"
    )


if __name__ == '__main__':
    print(statement(PARAMS))
    result = solve(PARAMS)
    print(f'solve(PARAMS) = {result}')
    print('VERIFY_PASS' if result == CANDIDATE else 'VERIFY_FAIL')
