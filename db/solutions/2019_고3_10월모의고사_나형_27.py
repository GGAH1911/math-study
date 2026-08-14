"""2019 고3 10월모의고사 나형 27번 — 파라미터화 솔버.

[원문제 수학 구조]
최고차항의 계수가 1인 삼차함수 f(x)에 대해
 (가) lim_{x→0} (f(x)-C)/x = 0
     → x→0 에서 극한이 존재하려면 f(0)=C 이어야 하고, 그때 극한값은 f'(0) 이므로
       f'(0)=0. 즉 f(x)=x^3+p x^2+C 꼴(1차항 계수 0)로 구조가 고정된다.
 (나) 곡선 y=f(x) 와 직선 y=L 의 교점의 개수가 2 이다.
     → x^3+p x^2+(C-L)=0 이 서로 다른 실근을 정확히 2개 가져야 하므로, 이 삼차식은
       "이중근 + 단순근" 구조를 가진다. 이는 이 삼차식의 판별식이 0이 되는 p 중,
       실제로 그렇게 되는 값을 골라야 한다(판별식 0 이라고 항상 실근 2개 구조는 아님).
 답: 구해진 p 로 f(X) 를 계산.

원문제는 C=3(=f(0)), L=-1(직선 y=-1), X=4(f(4) 를 구함) 인 경우이며,
이때 유일한 p=-3, f(x)=x^3-3x^2+3, f(4)=19 이다.

[파라미터로 뽑은 것]
 - C : 조건 (가)가 고정하는 f(0) 의 값 (그리고 lim 식의 상수항)
 - L : 조건 (나)의 직선 y=L
 - X : 최종적으로 구하는 f(X) 의 X
세 값 모두 최종 답을 바꾼다(직접 확인함, 아래 VARIANTS 참고).
"""
import sympy as sp

CANDIDATE = 19  # ★원문제 정답, 절대 바꾸지 않음

PARAMS = dict(C=3, L=-1, X=4)


def solve(prm):
    """조건 (가),(나) 로부터 p 를 실제로(sympy) 구하고 f(X) 를 반환."""
    C, L, X = sp.nsimplify(prm['C']), sp.nsimplify(prm['L']), sp.nsimplify(prm['X'])
    x, p = sp.symbols('x p', real=True)

    D = C - L  # x^3+p x^2+D=0 의 D = f(0)-L
    if D == 0:
        # 이 경우 이중근이 x=0 이 되어 앞서 유도한 (r,t)=(2r,...) 구조가
        # 별도 분기(원점 이중근)로 갈라져 문제의 전형적 구조가 깨진다.
        raise ValueError("C==L 이면 조건을 만족하는 삼차함수 구조가 성립하지 않습니다.")

    cubic = x**3 + p * x**2 + D

    # (나) '교점 2개'는 이 삼차식이 서로 다른 실근을 정확히 2개(이중근+단순근)
    # 갖는다는 뜻 → 판별식이 0 이 되는 p 를 실제로 풀고, 그중 진짜로
    # '이중근+단순근(distinct 2개)' 구조를 만드는 값만 채택한다.
    disc = sp.discriminant(cubic, x)
    cand_p = sp.solve(sp.Eq(disc, 0), p)

    valid = []
    for P in cand_p:
        P = sp.nsimplify(P)
        if abs(complex(sp.N(P)).imag) > 1e-9:
            continue  # 실수 p 만 후보
        cub_p = sp.expand(cubic.subs(p, P))
        real_roots = sp.Poly(cub_p, x).real_roots()  # 중복 포함, 정확한 대수적 실근
        if len(set(real_roots)) == 2:
            valid.append(P)

    if len(valid) != 1:
        raise ValueError(f"조건을 만족하는 p가 유일하지 않습니다: {valid}")

    P = valid[0]
    fX = sp.nsimplify((X**3 + P * X**2 + C))
    return fX


def statement(prm):
    C, L, X = prm['C'], prm['L'], prm['X']
    return (
        "최고차항의 계수가 1인 삼차함수 f(x)가 다음 조건을 만족시킬 때, "
        f"f({X})의 값을 구하시오. [4점]\n"
        "(가) " + r"\lim_{x \to 0} \frac{f(x)-" + f"{C}" + r"}{x} = 0" + "\n"
        f"(나) 곡선 y=f(x)와 직선 y={L}의 교점의 개수는 2이다."
    )


def _build(r, C, X):
    """이중근 값 r 을 정해서 (D=r^3/2 로) '깔끔한' L 을 만드는 보조 함수.
    solve() 자체는 이 r 을 모르고 C,L,X 만으로 실제 판별식을 풀어 p 를 구한다."""
    D = sp.Rational(r**3, 2)
    return dict(C=C, L=C - D, X=X)


VARIANTS = [
    dict(C=3, L=-1, X=4),        # 원문제: r=2 → p=-3, f(4)=19
    _build(r=4, C=3, X=4),       # r=4 → 다른 p, 다른 답
    _build(r=2, C=5, X=4),       # C 변경 → 다른 답
    _build(r=2, C=3, X=6),       # X 변경 → 다른 답
]


if __name__ == '__main__':
    print(statement(PARAMS))
    print('solve(PARAMS) =', solve(PARAMS))

    # 파라미터가 실제로 답을 바꾸는지 확인
    results = [solve(v) for v in VARIANTS]
    print('VARIANTS results =', results)
    assert len(set(results)) >= 3, "파라미터가 답을 충분히 바꾸지 않습니다."

    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
