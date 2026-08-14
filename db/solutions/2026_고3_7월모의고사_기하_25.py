# 점 A=(ax,ay) 를 지나고 방향벡터 u=(ux,uy) 인 직선 위의 점 P 에 대한 |OP| 의 최솟값.
# = 원점에서 그 직선까지의 거리. 최솟값을 실제로 구해 어느 보기와 같은지 판정한다.
# 원문제: A=(3√2,0), u=(1,2√2), 보기 ①8/3 ②3 ③10/3 ④11/3 ⑤4 → 최솟값 4 = 보기 ⑤
import sympy as sp

CANDIDATE = 5

PARAMS = dict(
    ax=3 * sp.sqrt(2),                       # 직선이 지나는 점의 x좌표
    ay=sp.Integer(0),                        # 직선이 지나는 점의 y좌표
    ux=sp.Integer(1),                        # 방향벡터 x성분
    uy=2 * sp.sqrt(2),                       # 방향벡터 y성분
    choices=(sp.Rational(8, 3), sp.Integer(3), sp.Rational(10, 3),
             sp.Rational(11, 3), sp.Integer(4)),   # 보기 값 (번호는 solve 가 판정)
)


def min_norm(prm):
    """직선 P(t) = A + t·u 위의 점에 대한 |OP| 의 최솟값 (원점-직선 거리)."""
    ax, ay = sp.sympify(prm['ax']), sp.sympify(prm['ay'])
    ux, uy = sp.sympify(prm['ux']), sp.sympify(prm['uy'])
    t = sp.symbols('t', real=True)
    P = sp.Matrix([ax + ux * t, ay + uy * t])
    d2 = sp.expand(P.dot(P))                      # |OP|^2 = 9t^2 + 6√2 t + 18 (원문제)
    crit = sp.solve(sp.diff(d2, t), t)            # d/dt |OP|^2 = 0
    if not crit:                                  # u = 0 → 직선이 아님
        return None
    mn2 = sp.simplify(d2.subs(t, crit[0]))
    return sp.nsimplify(sp.radsimp(sp.sqrt(sp.simplify(mn2))))


def solve(prm=PARAMS):
    """최솟값을 구해 보기와 대조하고 보기 번호를 돌려준다 (일치하는 보기가 없으면 0)."""
    mn = min_norm(prm)
    if mn is None:
        return 0
    for i, c in enumerate(prm['choices'], 1):
        if sp.simplify(mn - sp.sympify(c)) == 0:
            return i
    return 0


def statement(prm=PARAMS):
    """같은 유형의 새 문제 문장."""
    def tex(v):
        return sp.latex(sp.sympify(v))
    body = (f"점 $({tex(prm['ax'])},\\ {tex(prm['ay'])})$ 을 지나고 방향벡터가 "
            f"$\\vec{{u}}=({tex(prm['ux'])},\\ {tex(prm['uy'])})$ 인 직선 위의 점 $P$ 에 대하여 "
            f"$|\\vec{{OP}}|$ 의 최솟값은? (단, $O$ 는 원점이다.)")
    opts = '  '.join(f"{'①②③④⑤'[i]} ${tex(c)}$" for i, c in enumerate(prm['choices']))
    return f'{body}\n{opts}'


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
