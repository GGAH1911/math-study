"""
[원문제] f(x) = (2x-2)/(x^2-2x+2) = 2(x-1)/((x-1)^2+1)
  곡선 y=f(x)와 x축·y축으로 둘러싸인 영역 A, 곡선 y=f(x)와 x축·직선 x=3 으로
  둘러싸인 영역 B. A의 넓이 + B의 넓이 = ?  (①2ln2 ②ln6 ③3ln2 ④ln10 ⑤ln12)

[수학 구조]
  f(x) = k(x-a) / ((x-a)^2 + c^2)  는 x=a 에서 x절편을 갖고 점 (a,0) 에 대해
  기함수(점대칭) 구조이다: x<a 에서 f<=0, x>a 에서 f>=0.
    - 영역 A = y축(x=0) ~ x절편(x=a) 사이, x축 아래쪽 넓이  → A = -∫[0,a] f dx
    - 영역 B = x절편(x=a) ~ 직선 x=R 사이, x축 위쪽 넓이   → B =  ∫[a,R] f dx
  k=2 로 두면 부정적분이 ln((x-a)^2+c^2) 로 깔끔하게 떨어진다(분자가 분모의 도함수).
  따라서 문제를 결정하는 파라미터는 x절편 위치 a, 폭 상수 c, 오른쪽 경계선 R 이다.
  원문제는 a=1, c=1, R=3.

  보기 구성(값에서 유도): 정답 A+B 외에, "B를 놓치고 A만 두 배로 어림잡음"(2A),
  "B를 ln3 정도로 어림잡음"(A+ln3), "A만 세 배로 어림잡음"(3A), 그 조합(2A+ln3) 을
  전형적인 오답으로 삼는다. a=1,c=1,R=3 일 때 이 5개가 정확히 2ln2, ln6, 3ln2,
  ln10, ln12 로 원문제 보기와 일치한다(아래 assert 로 고정).
"""
import sympy as sp

x = sp.symbols('x', real=True)

CANDIDATE = 4          # ★원문제 정답(보기 번호) — 절대 바꾸지 않음
PARAMS = dict(a=1, c=1, R=3)   # a: x절편 위치, c: 분모 폭 상수, R: 오른쪽 경계선


def _areas(prm):
    """영역 A, B 의 넓이를 실제로 적분해서 구한다."""
    a, c, R = sp.nsimplify(prm['a']), sp.nsimplify(prm['c']), sp.nsimplify(prm['R'])
    if a <= 0:
        raise ValueError('a(x절편)는 0보다 커야 y축과의 사이에 영역 A가 생긴다')
    if R < a:
        raise ValueError('R은 a 이상이어야 영역 B가 정의된다')
    if c == 0:
        raise ValueError('c==0 이면 분모가 0이 되어 f(x)가 정의되지 않는다')
    f = 2 * (x - a) / ((x - a) ** 2 + c ** 2)
    A = sp.simplify(-sp.integrate(f, (x, 0, a)))
    B = sp.simplify(sp.integrate(f, (x, a, R)))
    return A, B


def value(prm):
    """수학적 답: 영역 A 넓이 + 영역 B 넓이."""
    A, B = _areas(prm)
    return sp.simplify(A + B)


def choices(prm):
    """보기 5개(값에서 유도). 정답(A+B) 과 전형적 오답 4개를 함께 만들고 오름차순 정렬."""
    A, B = _areas(prm)
    raw = [2 * A, A + sp.log(3), 3 * A, A + B, 2 * A + sp.log(3)]
    nums = [complex(sp.N(r)).real for r in raw]
    if len(set(round(n, 9) for n in nums)) != 5:
        raise ValueError('보기 5개 중 겹치는 값이 있어 문제로 성립하지 않는다')
    order = sorted(range(5), key=lambda i: nums[i])
    return [raw[i] for i in order]


def solve(prm):
    """조건 → 보기 번호."""
    A, B = _areas(prm)
    correct = sp.N(sp.simplify(A + B))
    cs = choices(prm)
    for i, cv in enumerate(cs, start=1):
        if abs(sp.N(cv) - correct) < 1e-9:
            return i
    raise ValueError('정답이 보기 중에 없다')


def statement(prm):
    a, c, R = prm['a'], prm['c'], prm['R']
    f = sp.together(2 * (x - a) / ((x - a) ** 2 + c ** 2))
    num, den = sp.fraction(f)
    num_s = str(sp.expand(num)).replace('**', '^').replace('*', '')
    den_s = str(sp.expand(den)).replace('**', '^').replace('*', '')
    labels = ['①', '②', '③', '④', '⑤']

    def fmt(e):
        e = sp.nsimplify(e)
        return str(e).replace('log', 'ln').replace('*', '')

    ch = ' '.join(f'{lab} {fmt(c_)}' for lab, c_ in zip(labels, choices(prm)))
    return (
        f'함수 f(x)=({num_s})/({den_s})에 대하여 곡선 y=f(x)와 x축 및 y축으로 '
        f'둘러싸인 영역을 A, 곡선 y=f(x)와 x축 및 직선 x={R}로 둘러싸인 영역을 B라 하자. '
        f'영역 A의 넓이와 영역 B의 넓이의 합은?\n{ch}'
    )


# ★원문제 보기 재현 확인(값에서 유도한 보기가 실제 원문제 보기와 같은지 고정)
_base = choices(PARAMS)
assert abs(sp.N(_base[0]) - sp.N(2 * sp.log(2))) < 1e-9   # ①2ln2
assert abs(sp.N(_base[1]) - sp.N(sp.log(6))) < 1e-9        # ②ln6
assert abs(sp.N(_base[2]) - sp.N(3 * sp.log(2))) < 1e-9    # ③3ln2
assert abs(sp.N(_base[3]) - sp.N(sp.log(10))) < 1e-9       # ④ln10 (정답)
assert abs(sp.N(_base[4]) - sp.N(sp.log(12))) < 1e-9       # ⑤ln12

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
