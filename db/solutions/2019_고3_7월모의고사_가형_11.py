import sympy as sp

# [문제 구조]
#   f(x) = a^{x-1} + k               (밑 a, 위로 k만큼 평행이동한 지수함수, k>0)
#     -> f(x)의 점근선: y = k
#   f^{-1}(x) = log_a(x-k) + 1        -> f^{-1}(x)의 점근선: x = k
#   g(x) = f^{-1}(x - c*k^p)          (f^{-1}을 x축 방향으로 c*k^p 만큼 평행이동)
#     -> g(x)의 점근선: x = k + c*k^p
#   두 점근선의 교점 (k + c*k^p, k) 가 직선 y = (m_num/m_den)*x 위에 있다.
#     => k = (m_num/m_den) * (k + c*k^p)   ... k>0 인 실근을 sympy로 직접 구한다.
#
#   원문제는 m_num/m_den=1/3, c=1, p=2 인 경우이며 이때 k=2.
#   보기는 k=2를 중심으로 한 등차수열(공차 1/2, 5개)이고 정답은 그 가운데(③)이다.
#   여기서는 "보기 격자(공차 step) 위에서 값이 어느 자리에 놓이는지"를 정수 나머지
#   연산으로 구해, 값이 바뀌면 정답 번호(선택지 위치)도 함께 바뀌도록 만들었다.
#   (밑 a는 점근선 계산에 전혀 영향을 주지 않으므로 파라미터로 넣지 않았다 - 실제로
#    답을 바꾸지 못하는 값을 PARAMS에 넣는 것은 규격 위반이다.)

CANDIDATE = 3  # 원문제 정답 번호 (보기 ③)

PARAMS = dict(
    m_num=1,     # 직선 y=(m_num/m_den)x 의 분자
    m_den=3,     # 직선 y=(m_num/m_den)x 의 분모
    c=1,         # g(x)를 만들 때의 평행이동량 계수: c*k^p
    p=2,         # 평행이동량의 k에 대한 지수
    step_num=1,  # 보기 등차수열의 공차(공차 = step_num/step_den)의 분자
    step_den=2,  # 보기 등차수열의 공차의 분모
)


def value(prm):
    """두 점근선의 교점이 직선 위에 있다는 조건으로 k를 실제로 방정식을 세워 푼다."""
    k = sp.Symbol('k', positive=True, real=True)
    m = sp.Rational(prm['m_num'], prm['m_den'])
    c = sp.nsimplify(prm['c'])
    p = prm['p']

    # 점근선 교점 (k + c*k^p, k) 가 직선 y = m*x 위에 있을 조건
    eq = sp.Eq(k, m * (k + c * k**p))

    sols = sp.solve(eq, k)
    sols = [sp.nsimplify(s) for s in sols if s.is_real and s > 0]
    if not sols:
        raise ValueError('조건을 만족하는 양의 실근이 없다')
    if len(sols) != 1:
        raise ValueError('조건을 만족하는 양의 실근이 유일하지 않다')
    return sols[0]


def choices(prm):
    """정답 값에서 등차수열 보기 5개를 유도하고, 값이 격자 위 몇 번째 자리인지로
    정답 번호를 정한다(격자 위에 있지 않으면 문제로 성립하지 않는 것으로 본다)."""
    v = value(prm)
    step = sp.Rational(prm['step_num'], prm['step_den'])
    q = v / step
    if not q.is_integer:
        raise ValueError('값이 보기 등차수열 격자 위에 놓이지 않는다')
    n = int(q)
    idx = ((n - 2) % 5) + 1  # 원문제(가운데, ③)에 맞춘 위상 보정
    base = v - (idx - 1) * step
    return [base + i * step for i in range(5)]


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    return ch.index(v) + 1


# 유도한 보기가 원문제의 보기(1, 3/2, 2, 5/2, 3)와 같은지 확인
assert choices(PARAMS) == [sp.Integer(1), sp.Rational(3, 2), sp.Integer(2),
                            sp.Rational(5, 2), sp.Integer(3)]


def statement(prm):
    m = sp.Rational(prm['m_num'], prm['m_den'])
    c = prm['c']
    p = prm['p']
    return (
        f"양수 k에 대하여 함수 f(x)=3^{{x-1}}+k의 역함수의 그래프를 x축의 방향으로 "
        f"{c}k^{{{p}}}만큼 평행이동시킨 곡선을 y=g(x)라 하자. 두 곡선 y=f(x), y=g(x)의 "
        f"점근선의 교점이 직선 y={sp.latex(m)}x 위에 있을 때, k의 값은?"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
