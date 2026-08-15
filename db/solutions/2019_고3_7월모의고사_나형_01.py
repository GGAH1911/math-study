"""
[원문제] 3 × 27^(1/3) 의 값은?  ① 6 ② 9 ③ 12 ④ 15 ⑤ 18   → 정답 ②(=2)

[수학 구조]
  값 = a × (c^n)^(1/n) = a × c   (a: 앞의 곱셈 계수, c: n제곱근 안의 밑, n: 근의 차수)
  27 = 3^3 이므로 a=3, c=3, n=3 → 값 = 3×3 = 9

  보기는 "계수 a 의 배수" 로 만들어져 있다: 6,9,12,15,18 = a×2, a×3, a×4, a×5, a×6.
  즉 보기 목록은 k = koffset..koffset+4 (koffset=2) 에 대한 a*k 이고,
  정답은 그 목록에서 값 a*c 가 놓이는 위치(1-indexed) 이다.

  koffset 을 흔들면 "값이 보기 중 몇 번째에 놓이는가"가 실제로 바뀌고,
  c 를 흔들면 값 자체가 달라져 역시 몇 번째 보기인지가 바뀐다 → 두 파라미터가
  진짜로 정답 번호를 움직이는 손잡이다. n 은 근의 차수(세제곱근/네제곱근 등)를
  바꿔도 c^n 구조상 값이 항상 a*c 로 귀결되므로 장식(문제 표현만 바뀜)이다.
"""
from sympy import Rational, Pow, simplify, nsimplify

CANDIDATE = 2   # ★원문제 정답: ②번 (절대 바꾸지 않음)

PARAMS = dict(
    a=3,        # 곱해지는 계수 (3 × ...)
    c=3,        # n제곱근 안의 밑 (27 = c^n 의 c)
    n=3,        # 근의 차수 (세제곱근이면 3)
    koffset=2,  # 보기 목록이 시작하는 배수 (2,3,4,5,6 배 중 시작값)
)


def value(prm):
    """근호 계산 결과: a × (c^n)^(1/n) = a × c."""
    a, c, n = prm['a'], prm['c'], prm['n']
    return simplify(a * Pow(c ** n, Rational(1, n)))


def choices(prm):
    """보기 목록: a 의 koffset..koffset+4 배."""
    a, koffset = prm['a'], prm['koffset']
    return tuple(a * k for k in range(koffset, koffset + 5))


def solve(prm):
    """값이 보기 목록에서 몇 번째(1-indexed)인지가 정답 번호다."""
    v = value(prm)
    opts = choices(prm)
    for i, o in enumerate(opts, start=1):
        if simplify(o - v) == 0:
            return i
    raise ValueError(f'값 {v} 가 보기 {opts} 안에 없음 — 성립하지 않는 문제')


def statement(prm):
    a, c, n, koffset = prm['a'], prm['c'], prm['n'], prm['koffset']
    opts = choices(prm)
    circled = ['①', '②', '③', '④', '⑤']
    opt_str = ' '.join(f'{circled[i]} {o}' for i, o in enumerate(opts))
    root = f'{c ** n}^{{\\frac{{1}}{{{n}}}}}'
    return f'{a} \\times {root}의 값은? {opt_str}'


# 원문제 보기(6,9,12,15,18)가 그대로 재현되는지 고정
assert choices(PARAMS) == (6, 9, 12, 15, 18), choices(PARAMS)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
