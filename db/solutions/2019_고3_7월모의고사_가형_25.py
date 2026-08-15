import sympy as sp

# 원문제 정답 (절대 변경 금지)
CANDIDATE = 8

# 문제의 수학 구조:
#   점 P(x, y)의 위치가 x = A*t + B*ln(t), y = (C/2)*t^2 + D*t 로 주어질 때,
#   dx/dt = dy/dt 를 만족하는 t(t>0)에서의 속도벡터의 크기 제곱 |v|^2 을 구한다.
#
#   원문제는 A=B=C=D=1 인 특수한 경우이다:
#     x = t + ln t,  y = (1/2)t^2 + t
#     dx/dt = 1 + 1/t,  dy/dt = t + 1
#     조건: 1/t = t → t^2 = 1 → t = 1 (t>0)
#     |v|^2 = 2^2 + 2^2 = 8
#
#   A, B, C, D 는 각각 x, y 를 이루는 항의 계수이며, 이 값들을 바꾸면
#   dx/dt = dy/dt 를 만족하는 t 의 값과 그 t 에서의 속도 성분이 함께 바뀌므로
#   최종 |v|^2 값도 달라진다.
PARAMS = dict(A=1, B=1, C=1, D=1)


def solve(prm):
    A = sp.nsimplify(prm['A'])
    B = sp.nsimplify(prm['B'])
    C = sp.nsimplify(prm['C'])
    D = sp.nsimplify(prm['D'])

    t = sp.symbols('t', positive=True, real=True)

    x = A * t + B * sp.log(t)
    y = sp.Rational(1, 2) * C * t**2 + D * t

    dx_dt = sp.diff(x, t)
    dy_dt = sp.diff(y, t)

    eq = sp.Eq(dx_dt, dy_dt)
    sols = sp.solve(eq, t)
    # t>0 실수인 해만 남긴다 (t 심볼이 positive=True 로 선언되어 있어
    # sympy 가 대체로 알아서 걸러주지만, 안전하게 한 번 더 확인한다)
    pos_sols = [s for s in sols if s.is_real and s.is_positive]

    if not pos_sols:
        raise ValueError(f'dx/dt = dy/dt 를 만족하는 t>0 인 해가 없습니다 (prm={prm})')
    if len(pos_sols) > 1:
        raise ValueError(f'해가 유일하지 않습니다: {pos_sols} (prm={prm})')

    t_val = pos_sols[0]
    v_x = dx_dt.subs(t, t_val)
    v_y = dy_dt.subs(t, t_val)

    v_squared = sp.simplify(v_x**2 + v_y**2)
    if not v_squared.is_number or v_squared.has(sp.zoo, sp.nan, sp.oo):
        raise ValueError(f'|v|^2 이 유효한 수가 아닙니다: {v_squared} (prm={prm})')
    return v_squared


def statement(prm):
    A, B, C, D = prm['A'], prm['B'], prm['C'], prm['D']
    return (
        '좌표평면 위를 움직이는 점 P의 시각 t(t > 0)에서의 위치 P(x, y)가\n'
        f'  x = {A} t + {B} \\ln t,  y = {sp.nsimplify(C)/2} t^2 + {D} t\n'
        '이다. dx/dt = dy/dt 일 때, 점 P의 속도를 \\vec{v}라 하자. '
        '|\\vec{v}|^2 의 값을 구하시오.'
    )


if __name__ == '__main__':
    print(statement(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
