# f(x)=cos(πx/a) (0≤x≤2a). 직선 y=c_hi 와의 교점 A,B / 직선 y=c_lo 와의 교점 C,D.
# 사각형 ACDB(윗변 AB, 아랫변 CD, 높이 c_hi-c_lo)의 넓이 조건으로 a 를 풀고 a×AB 를 구한다.
#
# ★파라미터화 솔버(scripts/CLAUDE.md 규격): PARAMS 의 수치를 바꾸면 같은 유형의
#   새 문제와 검증된 답이 그대로 나온다. 원문제는 PARAMS 기본값으로 재현된다.
CANDIDATE = 1
import sympy as sp

PARAMS = dict(
    c_hi=sp.Rational(1, 2),                 # 위쪽 직선 y=c_hi (교점 A,B)
    c_lo=sp.Rational(-1, 2),                # 아래쪽 직선 y=c_lo (교점 C,D)
    area=sp.Rational(3, 2),                 # 사각형 ACDB 의 넓이
    choices=(sp.Integer(3), sp.Rational(19, 6), sp.Rational(10, 3),
             sp.Rational(7, 2), sp.Rational(11, 3)),          # 보기 ①~⑤ 의 값
)


def _value(prm):
    """조건을 만족하는 a 와 그때의 a×AB 를 실제로 계산한다."""
    c_hi, c_lo, S = (sp.nsimplify(prm[k]) for k in ('c_hi', 'c_lo', 'area'))
    if not (-1 < c_lo < c_hi < 1) or S <= 0:
        raise ValueError('직선이 그래프와 두 점에서 만나지 않는 파라미터')
    a, x = sp.symbols('a x', positive=True)
    f = sp.cos(sp.pi * x / a)
    # 0≤x≤2a 에서 cos(πx/a)=c 의 두 근: x = (a/π)acos(c), 2a-(a/π)acos(c)
    A = a * sp.acos(c_hi) / sp.pi
    B = 2 * a - A
    C = a * sp.acos(c_lo) / sp.pi
    D = 2 * a - C
    for pt, val in ((A, c_hi), (B, c_hi), (C, c_lo), (D, c_lo)):
        assert sp.simplify(f.subs(x, pt) - val) == 0        # 교점이 실제로 그래프 위인지 확인
    AB, CD = sp.simplify(B - A), sp.simplify(D - C)
    height = c_hi - c_lo                                     # 두 직선 사이 거리
    area = sp.Rational(1, 2) * (AB + CD) * height            # 사다리꼴 ACDB
    a0 = [s for s in sp.solve(sp.Eq(area, S), a) if s.is_real and s > 0][0]
    return sp.simplify(a0), sp.simplify((a * AB).subs(a, a0))


def solve(prm):
    """답: 계산한 a×AB 가 보기에 있으면 그 보기 번호, 없으면(변형문제) 값 자체."""
    _, val = _value(prm)
    for i, ch in enumerate(prm['choices'], 1):
        if sp.simplify(val - sp.nsimplify(ch)) == 0:
            return sp.Integer(i)
    return sp.nsimplify(val)


def _choices_for(val):
    """변형문제용 보기 5개(정답 포함) — 정답 주변 등간격 distractor."""
    d = sp.nsimplify(val) / 6
    return tuple(sorted({sp.nsimplify(val) + k * d for k in (-2, -1, 0, 1, 2)}, key=float))


def statement(prm):
    a0, val = _value(prm)
    chs = prm['choices'] if any(sp.simplify(val - sp.nsimplify(c)) == 0
                                for c in prm['choices']) else _choices_for(val)
    opts = ' '.join(f'{"①②③④⑤"[i]} ${sp.latex(c)}$' for i, c in enumerate(chs))
    return (f"양수 $a$ 에 대하여 닫힌구간 $[0,\\,2a]$ 에서 정의된 함수 "
            f"$f(x)=\\cos\\dfrac{{\\pi x}}{{a}}$ 가 있다. 함수 $y=f(x)$ 의 그래프가 "
            f"직선 $y={sp.latex(sp.nsimplify(prm['c_hi']))}$ 과 만나는 두 점을 각각 $A$, $B$, "
            f"직선 $y={sp.latex(sp.nsimplify(prm['c_lo']))}$ 와 만나는 두 점을 각각 $C$, $D$ 라 하자. "
            f"사각형 $ACDB$ 의 넓이가 ${sp.latex(sp.nsimplify(prm['area']))}$ 일 때, "
            f"$a\\times\\overline{{AB}}$ 의 값은? (단, $A$ 의 $x$ 좌표는 $B$ 의 $x$ 좌표보다 작고, "
            f"$C$ 의 $x$ 좌표는 $D$ 의 $x$ 좌표보다 작다.)\n    {opts}"
            f"\n    [a={sp.latex(a0)}, 답 a×AB={sp.latex(val)}]")


print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
