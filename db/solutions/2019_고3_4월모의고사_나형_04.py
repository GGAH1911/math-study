import sympy as sp

# [원문제] y = √(2x) 의 그래프를 x축 방향으로 a만큼 평행이동하면 y = √(2x-4) 의
#   그래프와 일치한다. a의 값은? (정답 ②, 즉 a=2)
#
# [수학 구조]
#   y = √(k·x) 를 x축 방향으로 a만큼 평행이동 → y = √(k·(x-a)) = √(kx - ka)
#   이것이 y = √(kx - c) 와 일치 → k·a = c → a = c/k
#   여기서 k(원함수의 x계수, 이동 후에도 동일하게 유지)와 c(목표함수의 상수항)가
#   문제를 실제로 결정하는 파라미터다.
CANDIDATE = 2  # 원문제 정답: a = 2 (선택지 ②)

PARAMS = dict(
    k=2,  # y = √(k*x) 의 x 계수
    c=4,  # 평행이동 후 목표함수 y = √(k*x - c) 의 상수항
)


def value(prm):
    """a의 실제 값을 sympy로 방정식을 세워 구한다."""
    k = sp.nsimplify(prm['k'])
    c = sp.nsimplify(prm['c'])
    if k == 0:
        raise ValueError("k=0이면 함수가 상수가 되어 문제가 성립하지 않는다")

    x = sp.Symbol('x', real=True)
    a = sp.Symbol('a')

    original = sp.sqrt(k * x)
    shifted = original.subs(x, x - a)   # x축 방향으로 a만큼 평행이동: f(x) -> f(x-a)
    target = sp.sqrt(k * x - c)

    # √(k(x-a)) = √(kx-c) 이려면 두 근호 안의 식이 같아야 한다 (동일 정의역 전제)
    eq = sp.Eq(sp.expand(k * (x - a)), sp.expand(k * x - c))
    sols = sp.solve(eq, a)
    if not sols:
        raise ValueError("a에 대한 해가 존재하지 않는다")
    a_val = sp.nsimplify(sols[0])

    # 검증: 구한 a로 실제 두 함수가 (기호적으로) 일치하는지 확인
    if sp.simplify(shifted.subs(a, a_val) - target) != 0:
        raise ValueError("평행이동한 함수가 목표 함수와 일치하지 않는다")
    return a_val


def solve(prm):
    return value(prm)


def statement(prm):
    k = prm['k']
    c = prm['c']
    return (
        f"함수 y = √({k}x)의 그래프를 x축의 방향으로 a만큼 평행이동하면 "
        f"함수 y = √({k}x-{c})의 그래프와 일치한다. 상수 a의 값은?"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
