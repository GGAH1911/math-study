"""2019 고3 7월모의고사 나형 4번 — 파라미터화 솔버.

문제 구조: 유한집합 X(정의역)에서 유한집합 Y(공역)로 가는 전단사함수 f 가 그림(대응 화살표)
으로 주어지고, f(a) + f^{-1}(b) 의 값을 구해 5지선다 중 몇 번째 보기인지 고른다.

파라미터로 뽑은 수학적 손잡이:
  - domain / codomain_map : 그림 속 대응 f(1),f(2),f(3),f(4) 자체 (전단사 permutation)
  - a, b                  : f(a) 와 f^{-1}(b) 를 물을 때의 입력값
  - lowest_choice         : 보기 ①의 값 (보기는 이 값부터 시작하는 연속된 정수 5개)
    → f(a)+f^{-1}(b) 의 값이 이 5개 보기 중 몇 번째(①~⑤)에 오는지를
      sympy 로 1차방정식 lowest_choice + (n-1) = value 를 풀어 n(보기 번호)을 구한다.

원문제: f: 1→4, 2→3, 3→2, 4→5, a=2, b=3, 보기는 3,4,5,6,7 (①=3부터 시작).
  f(2)=3, f^{-1}(3)=2 → 값=5 → 보기 중 3번째(③). CANDIDATE=3.
"""
import sympy as sp

CANDIDATE = 3

PARAMS = dict(
    domain=(1, 2, 3, 4),        # X: 정의역 원소들 (그림 왼쪽 점들)
    codomain_map=(4, 3, 2, 5),  # f(1),f(2),f(3),f(4) — 그림의 화살표 대응 (전단사)
    a=2,                        # f(a) 를 구할 입력
    b=3,                        # f^{-1}(b) 를 구할 입력
    lowest_choice=3,            # 보기 ①의 값 (보기 = lowest_choice, +1, +2, +3, +4)
)


def _build_f(prm):
    dom, vals = prm['domain'], prm['codomain_map']
    if len(dom) != len(vals):
        raise ValueError('정의역과 대응값의 개수가 다르다')
    if len(set(dom)) != len(dom) or len(set(vals)) != len(vals):
        raise ValueError('f 가 전단사가 아니다 (정의역 또는 공역에 중복)')
    return dict(zip(dom, vals))


def value(prm):
    """f(a) + f^{-1}(b) 를 sympy 정수로 계산한다."""
    f = _build_f(prm)
    finv = {v: k for k, v in f.items()}
    a, b = prm['a'], prm['b']
    if a not in f:
        raise ValueError('a 가 정의역 밖이다')
    if b not in finv:
        raise ValueError('b 가 f 의 치역 밖이라 f^{-1}(b) 가 없다')
    return sp.Integer(f[a]) + sp.Integer(finv[b])


def choices(prm):
    """lowest_choice 부터 시작하는 연속된 정수 5개 (①~⑤)."""
    lo = sp.Integer(prm['lowest_choice'])
    return tuple(lo + k for k in range(5))


def solve(prm):
    """값이 보기 중 몇 번째(①=1 ... ⑤=5)인지 sympy 로 방정식을 풀어 구한다."""
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError('값이 보기 범위를 벗어난다')
    lo = sp.Integer(prm['lowest_choice'])
    n = sp.symbols('n', positive=True)
    sol = sp.solve(sp.Eq(lo + (n - 1), v), n)
    if not sol:
        raise ValueError('보기 번호를 구하는 방정식에 해가 없다')
    idx = sol[0]
    if idx != sp.floor(idx) or idx < 1 or idx > 5:
        raise ValueError('보기 번호가 유효 범위를 벗어난다')
    return int(idx)


def statement(prm):
    f = _build_f(prm)
    dom = prm['domain']
    arrows = ', '.join(f'{k}\\to{f[k]}' for k in dom)
    ch = choices(prm)
    ch_str = ' '.join(f'{i+1} {v}' for i, v in enumerate(ch))
    return (
        f"함수 f : X \\rightarrow Y 가 대응 $f:{arrows}$ 로 주어져 있다.\n"
        f"f({prm['a']}) + f^{{-1}}({prm['b']}) 의 값은?\n"
        f"[보기 번호-값] {ch_str}"
    )


assert value(PARAMS) == 5
assert choices(PARAMS) == (3, 4, 5, 6, 7)
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
