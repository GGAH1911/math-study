# 공간에 점 A 에서 서로 수직으로 만나는 두 직선 l, m 을 품은 평면 α 가 있다.
# α 위에 있지 않은 점 P 에서 l, m 에 내린 수선의 발이 각각 B, C 이고 AB, AC, PA 가 주어진다.
# 삼각형 ABC 의 평면 PBC 위로의 정사영의 넓이를 구한다.
#
# 좌표화: A=원점, l=x축, m=y축, α: z=0.  B=(p,0,0), C=(0,q,0).
#   P 에서 x축(=l)에 내린 수선의 발이 B → P 의 x좌표 = p
#   P 에서 y축(=m)에 내린 수선의 발이 C → P 의 y좌표 = q      ⇒ P=(p, q, h)
#   PA=d 에서 p^2+q^2+h^2=d^2 이므로 h=sqrt(d^2-p^2-q^2)  (P 가 α 밖 ⇒ d^2 > p^2+q^2)
# 정사영의 넓이 = |△ABC| · cos(평면 ABC 와 평면 PBC 가 이루는 각)
#   → 두 평면의 법선(외적)으로 cos 을 잡아 결정적으로 계산한다.
import sympy as sp

CANDIDATE = 3          # 정답 = 보기 ③

PARAMS = dict(
    AB=2*sp.sqrt(3),                 # A 에서 직선 l 위의 수선의 발 B 까지의 거리
    AC=sp.Integer(2),                # A 에서 직선 m 위의 수선의 발 C 까지의 거리
    PA=sp.Integer(5),                # 공간의 점 P 에서 A 까지의 거리 (> sqrt(AB^2+AC^2))
    choices=[sp.sqrt(3)/3, sp.sqrt(6)/2, sp.sqrt(3), 2*sp.sqrt(2), 4*sp.sqrt(6)/3],
)


def height(prm):
    """평면 α 에서 점 P 까지의 높이 h (주어진 조건에서 유도되는 값)."""
    p, q, d = (sp.nsimplify(prm[k]) for k in ('AB', 'AC', 'PA'))
    h = sp.symbols('h', positive=True)
    return sp.solve(sp.Eq(p**2 + q**2 + h**2, d**2), h)[0]


def projected_area(prm):
    """삼각형 ABC 의 평면 PBC 위로의 정사영의 넓이 (정확값)."""
    p, q = sp.nsimplify(prm['AB']), sp.nsimplify(prm['AC'])
    h = height(prm)
    A = sp.Matrix([0, 0, 0])
    B = sp.Matrix([p, 0, 0])
    C = sp.Matrix([0, q, 0])
    P = sp.Matrix([p, q, h])
    n1 = (B - A).cross(C - A)                    # 평면 ABC 의 법선
    n2 = (B - P).cross(C - P)                    # 평면 PBC 의 법선
    cos = sp.Abs(n1.dot(n2)) / (n1.norm() * n2.norm())
    area_ABC = sp.Rational(1, 2) * n1.norm()
    return sp.radsimp(sp.simplify(area_ABC * cos))


def solve(prm=PARAMS):
    """객관식 답. 정사영의 넓이를 보기와 대조해 **보기 번호**를 돌려준다.
    보기에 그 값이 없으면(유사문제 생성 중) 넓이 값 자체를 돌려준다."""
    value = projected_area(prm)
    for i, c in enumerate(prm.get('choices') or [], 1):
        if sp.simplify(value - sp.nsimplify(c)) == 0:
            return i
    return value


def statement(prm):
    """같은 유형의 새 문제 문장."""
    p, q, d = (sp.latex(sp.nsimplify(prm[k])) for k in ('AB', 'AC', 'PA'))
    body = ('공간에 점 A에서 서로 수직으로 만나는 두 직선 l, m을 포함하는 평면 α가 있다. '
            '평면 α 위에 있지 않은 점 P에서 두 직선 l, m에 내린 수선의 발을 각각 B, C라 할 때, '
            f'$\\overline{{AB}}={p}$, $\\overline{{AC}}={q}$이다. $\\overline{{PA}}={d}$일 때, '
            '삼각형 ABC의 평면 PBC 위로의 정사영의 넓이는? '
            '(단, 점 B는 점 A가 아니고, 점 C는 점 A가 아니다.)')
    ch = prm.get('choices') or []
    if ch:
        body += ' ' + ' '.join(f'{"①②③④⑤"[i]}${sp.latex(sp.nsimplify(c))}$' for i, c in enumerate(ch))
    return body


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
