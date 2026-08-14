import sympy as sp

# ============================================================
# 문제 구조
#   자연수 n에 대해, 한 변의 길이가 1이고 꼭짓점이 격자점인 정사각형 중에서
#   연립부등식  (1/2)x^2 < y < u*x^2,  0 < x < 2*k2*n - s
#   를 만족하는 점 (x,y)(실수)를 내부에 하나라도 포함하는 것의 개수를 S_n이라 할 때,
#       lim_{n->∞} (S_{n+1}-S_n)/n^2
#   을 구한다.
#
#   원문제는 u=1 (위쪽 경계 x^2), k2=1 (x-범위 계수 2), s=1 (x-범위 "-1") 인 경우.
#
# 파라미터화 아이디어
#   - u   : 위쪽 경계 곡선의 계수  y < u*x^2   (원문제 1)
#   - k2  : x-범위 "0<x<2*k2*n - s" 의 n-계수를 2*k2 로 둔 값   (원문제 1, 즉 계수=2)
#   - s   : x-범위의 상수 이동값(홀수, 원문제 1)
#
#   정수 격자점 x=a (a=0,...,M-1, M=2*k2*n-s)로 나뉘는 각 세로줄에서, 그 줄
#   (x∈(a,a+1)) 위의 영역이 차지하는 y-구간은 두 곡선이 단조증가이므로
#   ( (1/2)a^2 , u*(a+1)^2 ) 로 이어진 하나의 구간이 된다 (겹침 없이 연속으로 이어짐).
#   이 구간과 겹치는 정사각형(=정수 b)의 개수는
#       count(a) = ceil(u*(a+1)^2) - floor((1/2)*a^2)
#   이며, a의 홀짝에 따라 floor 값이 정수/반정수로 나뉘므로 a=2m, a=2m+1로 나누어
#   등차수열의 합(시그마)을 sympy로 직접 계산해 S_n의 닫힌 식(n에 대한 3차식)을 얻고,
#   그 후 극한을 sympy로 계산한다. u, k2 를 바꾸면 답이 실제로 바뀐다(아래 검증).
#   s는 문제가 성립하기 위한(=x-범위가 홀수 개의 세로줄을 갖도록 하는) 구조적 값으로,
#   S_n의 저차항(및 유한 n에서의 실제 값)에는 영향을 주지만 극한값 자체는 바꾸지
#   않는다 — 이는 우연이 아니라 극한이 S_n의 최고차항(3차항 계수)에만 의존하기
#   때문이며, s 역시 solve() 내부에서 실제로 사용되어 S_n 계산에 관여한다.
# ============================================================

CANDIDATE = 4

PARAMS = dict(u=1, k2=1, s=1)


def _S_n_formula(u, k2, s):
    """sympy로 S_n(n)의 닫힌 식(3차 다항식)을 유도한다."""
    if not (isinstance(u, int) and u >= 1):
        raise ValueError("u는 1 이상의 정수여야 합니다 (위쪽 경계 y<u*x^2).")
    if not (isinstance(k2, int) and k2 >= 1):
        raise ValueError("k2는 1 이상의 정수여야 합니다.")
    if not (isinstance(s, int) and s >= 1 and s % 2 == 1):
        raise ValueError("s는 1 이상의 홀수여야 합니다 (x-범위 세로줄 개수를 홀수로 유지).")
    if s >= 2 * k2:
        # n=1일 때조차 M=2*k2*1-s > 0 이어야 문제(영역)가 존재한다.
        raise ValueError("s < 2*k2 이어야 n=1부터 영역이 존재합니다.")

    m, n = sp.symbols('m n', integer=True, nonnegative=True)
    c1 = sp.Rational(1, 2)
    c2 = sp.Integer(u)

    # 세로줄 x=a, a=2m (짝수)
    a_even = 2 * m
    L_even = sp.floor(c1 * a_even ** 2)
    U_even = sp.ceiling(c2 * (a_even + 1) ** 2)
    count_even = sp.expand(sp.simplify(U_even - L_even))

    # 세로줄 x=a, a=2m+1 (홀수)
    a_odd = 2 * m + 1
    L_odd = sp.floor(c1 * a_odd ** 2)
    U_odd = sp.ceiling(c2 * (a_odd + 1) ** 2)
    count_odd = sp.expand(sp.simplify(U_odd - L_odd))

    M = 2 * k2 * n - s  # 세로줄(정사각형의 x-열) 개수, a=0,...,M-1  (M은 홀수)
    upper_even = sp.simplify((M - 1) / 2)   # 짝수 a=0,2,...,M-1 -> m의 최댓값
    upper_odd = sp.simplify((M - 3) / 2)    # 홀수 a=1,3,...,M-2 -> m의 최댓값

    S_even = sp.Sum(count_even, (m, 0, upper_even)).doit()
    S_odd = sp.Sum(count_odd, (m, 0, upper_odd)).doit()
    S_n = sp.expand(sp.simplify(S_even + S_odd))
    return S_n, n


def solve(prm):
    u, k2, s = prm['u'], prm['k2'], prm['s']
    S_n, n = _S_n_formula(u, k2, s)
    S_np1 = S_n.subs(n, n + 1)
    diff = sp.expand(sp.simplify(S_np1 - S_n))
    lim = sp.limit(diff / n ** 2, n, sp.oo)
    if not lim.is_finite:
        raise ValueError("극한이 존재하지 않습니다.")
    return int(lim)


def statement(prm):
    u, k2, s = prm['u'], prm['k2'], prm['s']
    upper = f"{u}x^{{2}}" if u != 1 else "x^{2}"
    mult = 2 * k2
    xrange = f"{mult}n - {s}" if mult != 1 else f"n - {s}"
    return (
        "자연수 n에 대하여 다음 조건을 만족시키는 정사각형의 개수를 S_{n}이라 하자.\n"
        "(가) 정사각형은 한 변의 길이가 1이고 꼭짓점의 x좌표와 y좌표가 모두 정수이다.\n"
        f"(나) 연립부등식 \\frac{{1}}{{2}}x^{{2}} < y < {upper}, 0 < x < {xrange}"
        "을 만족시키는 점 (x, y) 중에는 정사각형의 내부에 있는 점이 있다.\n"
        "\\lim_{n \\to \\infty} \\frac{S_{n+1}-S_{n}}{n^{2}}의 값을 구하시오."
    )


if __name__ == '__main__':
    # 원문제 재현 검증
    assert solve(PARAMS) == CANDIDATE

    # 답을 실제로 바꾸는 파라미터 확인: u, k2 각각을 바꾸면 값이 달라진다.
    base = solve(dict(u=1, k2=1, s=1))
    v_u = solve(dict(u=2, k2=1, s=1))
    v_k2 = solve(dict(u=1, k2=2, s=1))
    assert v_u != base, "u를 바꿔도 답이 그대로면 안 됨"
    assert v_k2 != base, "k2를 바꿔도 답이 그대로면 안 됨"

    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
