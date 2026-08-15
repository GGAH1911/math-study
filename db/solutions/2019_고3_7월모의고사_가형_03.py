"""2점 좌표공간 문제 — 파라미터화 솔버.

원문제: A(1,0,2), B(2,0,a) 에 대하여 선분 AB를 1:2로 외분하는 점이 원점일 때 a의 값은?
        ①3 ②4 ③5 ④6 ⑤7   (정답 ②, 즉 값은 4)

수학 구조:
  A=(x1,y1,z1), B=(x2,y2,a) (x1,y1,x2,y2 는 도형을 단순하게 유지하려고 고정값으로 둔다).
  선분 AB를 m:n 으로 외분하는 점 = ((m*x2-n*x1)/(m-n), (m*y2-n*y1)/(m-n), (m*a-n*z1)/(m-n)).
  x,y 좌표는 A,B,m,n 만으로 이미 결정되므로 그대로 유도해 문제 문장에 쓰고,
  z 좌표가 목표점의 z좌표 tz 와 같아야 한다는 조건 하나로 미지수 a 를 sympy 로 구한다.

  살아있는(답을 바꾸는) 파라미터:
    z1 : A의 z좌표 — a 의 값 자체를 바꾼다.
    tz : 외분점(목표점)의 z좌표(원문제는 원점이므로 0) — a 의 값 자체를 바꾼다.
    m,n : 외분비(m:n) — a 의 값을 바꾸는 동시에, 보기 목록에서 정답이 놓이는 자리도
          (n-m) mod 5 로 바뀐다(원문제에서 실제 보기 배치 ①3 ②4 ③5 ④6 ⑤7 과 일치하도록
          역산해 얻은 회전식 — work1 계열 솔버와 동일한 관례).
"""
import sympy as sp

CANDIDATE = 2  # ★원문제 정답(보기 번호) — 절대 바꾸지 않는다

# 문제를 정하는 값들: z1(A의 z좌표), m,n(외분비 m:n), tz(외분점의 z좌표)
PARAMS = dict(z1=2, m=1, n=2, tz=0)

# A,B 의 x,y 좌표는 도형을 단순히 유지하려는 고정 상수(문제 문장 표시에만 쓰인다)
_X1, _Y1, _X2, _Y2 = 1, 0, 2, 0


def value(prm):
    """조건을 만족하는 a 의 실제 값(sympy 로 계산)."""
    z1 = sp.Integer(prm['z1'])
    m = sp.Integer(prm['m'])
    n = sp.Integer(prm['n'])
    tz = sp.Integer(prm['tz'])
    if m == n:
        raise ValueError('m == n 이면 외분점이 정의되지 않는다')

    a = sp.symbols('a')
    # 외분점 z좌표 = (m*a - n*z1)/(m-n) 이 tz 와 같아야 한다
    eq = sp.Eq((m * a - n * z1) / (m - n), tz)
    sol = sp.solve(eq, a)
    if len(sol) != 1:
        raise ValueError('해가 유일하지 않다')
    return sp.nsimplify(sol[0])


def _pos0(prm):
    """보기 5개 중 정답이 놓이는 0-based 자리. (n-m) mod 5 로 정답 위치가 결정된다.

    ★원문제(m=1,n=2)에서 (n-m) mod 5 = 1 → 정답이 두 번째(②) 자리에 오도록 역산했다.
    """
    m = sp.Integer(prm['m'])
    n = sp.Integer(prm['n'])
    return int((n - m) % 5)


def choices(prm):
    """정답 주변의 연속한 정수 5개 — 정답의 자리는 _pos0 로 정해진다."""
    v = value(prm)
    pos0 = _pos0(prm)
    smallest = v - pos0
    return tuple(smallest + i for i in range(5))


def solve(prm):
    """value(prm) 이 choices(prm) 중 몇 번째(1~5)인지 = 보기 번호."""
    v = value(prm)
    cs = choices(prm)
    for i, c in enumerate(cs, start=1):
        if sp.simplify(c - v) == 0:
            return i
    raise ValueError('value 가 choices 안에 없다')


def statement(prm):
    z1, m, n, tz = prm['z1'], prm['m'], prm['n'], prm['tz']
    x1, y1, x2, y2 = _X1, _Y1, _X2, _Y2
    tx = sp.nsimplify((sp.Integer(m) * x2 - sp.Integer(n) * x1) / (sp.Integer(m) - sp.Integer(n)))
    ty = sp.nsimplify((sp.Integer(m) * y2 - sp.Integer(n) * y1) / (sp.Integer(m) - sp.Integer(n)))
    cs = choices(prm)
    opts = ' '.join(f'{c}' for c in ['①', '②', '③', '④', '⑤'])
    labeled = ' '.join(f'{lab}{val}' for lab, val in zip(['①', '②', '③', '④', '⑤'], cs))
    return (
        f"좌표공간의 두 점 A({x1}, {y1}, {z1}), B({x2}, {y2}, a)에 대하여\n"
        f"  선분 AB를 {m} : {n}로 외분하는 점이 ({tx}, {ty}, {tz})일 때, a의 값은?\n"
        f"  {labeled}"
    )


# 원문제(디폴트 파라미터)에서 보기 목록이 실제 보기(①3 ②4 ③5 ④6 ⑤7)와 정확히 같은지 고정한다.
assert choices(PARAMS) == (3, 4, 5, 6, 7), f'보기 재현 실패: {choices(PARAMS)}'

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
