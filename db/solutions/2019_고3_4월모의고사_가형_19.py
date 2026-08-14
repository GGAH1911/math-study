"""
[원문제] 19. 그림과 같이 AB=1, angle B=pi/2 인 직각삼각형 ABC 에서 선분 AB 위에
AD=CD 가 되도록 점 D를 잡는다. 점 D에서 선분 AC에 내린 수선의 발을 E,
점 D를 지나고 직선 AC에 평행한 직선이 선분 BC와 만나는 점을 F라 하자.
angle BAC=theta 일 때 삼각형 DEF의 넓이를 S(theta)라 하자.
lim_{theta->0+} S(theta)/theta 의 값은?   [정답] 4번째 보기 = 1/8

[수학 구조]
  A=(0,0), B=(b,0), C=(b, b*tan(theta)) 로 좌표를 잡으면 (angle B=pi/2, AB=b, angle BAC=theta)
    - AD=CD 조건으로 D=(b*sec^2(theta)/2, 0)
    - E = D에서 AC로 내린 수선의 발, F = D를 지나 AC와 평행한 직선과 BC의 교점
    - S(theta,b) = 삼각형 DEF 넓이, lim_{theta->0+} S(theta,b)/theta = b**2/8
      (아래 _limit_value_symbolic() 에서 sympy solve+limit 으로 직접 유도)
  즉, 빗변을 이루는 변의 길이 AB=b 를 일반화하면 정답 자체가 b**2/8 로 실제
  바뀐다 (b=1일 때 원문제의 1/8).

[파라미터화 포인트]
  - b     : AB의 길이. 최종 값(=b**2/8)을 실제로 바꾸는 진짜 기하 파라미터.
  - n0    : 보기 5개를 만드는 등차 격자(n/denom, n=n0..n0+4)의 시작 분자.
            원문제 보기 (1/32,1/16,3/32,1/8,5/32) 는 n=1..5, denom=32 인 격자다.
  - denom : 격자의 분모. n0, b 와 함께 정답이 보기 중 몇 번째(=solve의 반환값)에
            놓이는지를 실제로 결정한다.
"""
from sympy import (symbols, Eq, solve as sp_solve, simplify, trigsimp, Abs, tan,
                    limit, Rational, Matrix)

CANDIDATE = 4  # 원문제 정답: 4번째 보기(1/8) — 절대 바꾸지 않음

PARAMS = dict(
    b=1,       # AB의 길이
    n0=1,      # 보기 격자 시작 분자
    denom=32,  # 보기 격자 분모
)


def _limit_value_symbolic():
    """AB=B(양수 기호)로 두고 실제 sympy 계산(연립방정식 풀이 + 극한)으로
    lim_{theta->0+} S(theta)/theta = B**2/8 임을 유도한다. (한 번만 계산)"""
    theta, B = symbols('theta B', positive=True)
    xD = symbols('xD', positive=True)

    A = Matrix([0, 0])
    C = Matrix([B, B * tan(theta)])
    D = Matrix([xD, 0])

    # AD = CD  ->  AD^2 = CD^2 를 풀어서 D의 x좌표를 구한다
    AD2 = (D - A).dot(D - A)
    CD2 = (D - C).dot(D - C)
    xD_sol = sp_solve(Eq(AD2, CD2), xD)[0]
    D = D.subs(xD, xD_sol)

    # E: D에서 직선 AC(방향 dirv)에 내린 수선의 발 (정사영)
    dirv = C - A
    t = (D.dot(dirv)) / (dirv.dot(dirv))
    E = simplify(t * dirv)

    # F: D를 지나 AC에 평행한 직선과 BC(x=B)의 교점
    s = symbols('s')
    s_val = sp_solve(Eq(D[0] + s * dirv[0], B), s)[0]
    F = simplify(D + s_val * dirv)

    def cross2(u, v):
        return u[0] * v[1] - u[1] * v[0]

    DE, DF = E - D, F - D
    area = trigsimp(simplify(Rational(1, 2) * Abs(cross2(DE, DF))))

    return simplify(limit(area / theta, theta, 0, '+')), B


_GENERAL_VALUE, _B_SYM = _limit_value_symbolic()


def value(prm):
    """AB=b 일 때 lim_{theta->0+} S(theta)/theta 값
    (sympy로 유도된 일반식 _GENERAL_VALUE 에 b를 대입)."""
    return simplify(_GENERAL_VALUE.subs(_B_SYM, prm['b']))


def choices(prm):
    """보기 5개: n/denom (n=n0..n0+4) 등차 격자에서 정답이 놓일 자리만
    실제 value(prm) 으로 채운다. b, n0 를 바꾸면 정답의 위치(=solve의
    반환값)가 실제로 바뀐다."""
    n0, denom = prm['n0'], prm['denom']
    v = value(prm)

    target = simplify(v * denom)
    if not target.is_integer:
        raise ValueError('격자에 정확히 맞아떨어지지 않는 조합')
    idx0 = int(target - n0) % 5

    lst = []
    for j in range(5):
        if j == idx0:
            lst.append(v)
        else:
            lst.append(Rational(n0 + j, denom))
    return lst


def solve(prm):
    """보기 중 정답의 번호(1~5)를 반환한다."""
    v = value(prm)
    ch = choices(prm)
    for i, c in enumerate(ch, start=1):
        if simplify(c - v) == 0:
            return i
    raise ValueError('정답이 보기 목록에 없음 - 유효하지 않은 파라미터 조합')


def statement(prm):
    b = prm['b']
    ch = choices(prm)
    marks = ['①', '②', '③', '④', '⑤']
    opts = '  '.join(f'{m} {c}' for m, c in zip(marks, ch))
    return (
        f"그림과 같이 \\overline{{AB}}={b}, \\angle B=\\frac{{\\pi}}{{2}}인 직각삼각형 ABC에서 "
        f"선분 AB 위에 \\overline{{AD}}=\\overline{{CD}}가 되도록 점 D를 잡는다. "
        f"점 D에서 선분 AC에 내린 수선의 발을 E, 점 D를 지나고 직선 AC에 평행한 직선이 "
        f"선분 BC와 만나는 점을 F라 하자. \\angle BAC=\\theta일 때, 삼각형 DEF의 넓이를 "
        f"S(\\theta)라 하자. \\lim_{{\\theta \\to 0^+}} \\frac{{S(\\theta)}}{{\\theta}}의 값은?\n{opts}"
    )


# 원문제 보기(1/32, 1/16, 3/32, 1/8, 5/32)를 그대로 재현하는지 고정
assert choices(PARAMS) == [Rational(1, 32), Rational(1, 16), Rational(3, 32), Rational(1, 8), Rational(5, 32)]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
