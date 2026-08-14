"""
함수 f(x) = c/(b·x - d) + a 의 정의역과 치역이 서로 같을 때, 상수 a 의 값.

수학 구조 (원문제: c=4, b=2, d=7):
  정의역 = R \\ {d/b}            ← 분모 b·x - d 의 영점
  치역   = R \\ {a}              ← y = c/(b·x - d) + a 를 x 에 대해 풀면
                                  x = d/b + c/(b·(y-a)) 이므로 y = a 에서 정의 불가
  정의역 = 치역  ⟺  a = d/b     ← 정답 (b, d 만으로 결정)

파라미터로 뽑은 값 (문제를 정하는 값):
  c : 분자 — 구조 파라미터 (c ≠ 0 조건만; 답 a = d/b 에는 영향 없음)
  b : 분모의 x 계수 — 답을 바꿈 (살아있는 파라미터)
  d : 분모 상수     — 답을 바꿈 (살아있는 파라미터)

보기 생성 (값/파라미터에서 유도 — 고정 튜플 금지):
  학생이 흔히 내는 오답 후보 4개 + 정답 d/b 를 정렬해 보기로 만든다.
    (d-4)/b, b, (d-2)/b, (d-4)/(b-1), d/b(정답)
  원문제 (c,b,d) = (4,2,7) 에서 정렬하면 정확히 (3/2, 2, 5/2, 3, 7/2) 가 되고
  정답 7/2 는 ⑤번 → CANDIDATE = 5.
  파라미터를 바꾸면 후보 (d-4)/(b-1) 가 정답 d/b 를 기준으로 위치를 달리해
  정답의 보기 번호가 실제로 바뀐다 (예: d > 4b 또는 d < b² 이면 정답이 ④번으로 이동).
"""

# 주의: sympy 의 solve 는 아래 `def solve(prm)` 과 이름이 겹치므로 반드시 별칭으로 import.
from sympy import symbols, Eq, solve as sp_solve, simplify, Rational, fraction

CANDIDATE = 5  # 원문제 정답: ⑤ 7/2 — ★절대 변경 금지

# 문제를 정하는 값들: f(x) = c/(b·x - d) + a
PARAMS = {'c': 4, 'b': 2, 'd': 7}


def _validate(prm):
    c, b, d = prm['c'], prm['b'], prm['d']
    if c == 0:
        raise ValueError('c=0 이면 상수함수가 되어 치역이 한 점 — 문제 성립 안 함')
    if b <= 1:
        raise ValueError('b는 1보다 큰 자연수여야 함 (b=1 이면 보기 (d-4)/(b-1) 정의 불가)')
    if d <= 0:
        raise ValueError('d는 양수여야 함')


def value(prm):
    """수학적 답: '정의역 = 치역' 조건을 sympy 로 실제로 풀어 a = d/b 를 얻는다."""
    _validate(prm)
    c, b, d = Rational(prm['c']), Rational(prm['b']), Rational(prm['d'])
    x, y, a = symbols('x y a')
    # 1) 정의역의 제외점: 분모 b·x - d = 0  →  x = d/b
    dom_excl = sp_solve(Eq(b * x - d, 0), x)[0]
    # 2) 치역: y = c/(b·x - d) + a 를 x 에 대해 역산
    xsol = sp_solve(Eq(y, c / (b * x - d) + a), x)[0]      # x = d/b + c/(b·(y-a)) 꼴
    # 3) x 가 정의되지 않는 y 값 = 역산 분모의 영점  →  y = a  (치역 제외점)
    range_excl = sp_solve(Eq(fraction(xsol)[1], 0), y)[0]
    # 4) 정의역 = 치역  ⟺  제외점 일치  →  a = d/b
    return simplify(sp_solve(Eq(dom_excl, range_excl), a)[0])


def choices(prm):
    """보기 목록: 오답 후보 4개 + 정답을 정렬해 생성 (값에서 유도)."""
    _validate(prm)
    b, d = Rational(prm['b']), Rational(prm['d'])
    cands = [
        (d - 4) / b,       # 후보 ①: 분자/분모 단순 조작   → 원문제 3/2
        b,                 # 후보 ②: x 계수를 a 로 오인    → 원문제 2
        (d - 2) / b,       # 후보 ③: 분자/분모 단순 조작   → 원문제 5/2
        (d - 4) / (b - 1), # 후보 ④: 분모를 (b-1) 로 잘못 봄 → 원문제 3
        value(prm),        # 정답 ⑤: a = d/b               → 원문제 7/2
    ]
    if len(set(cands)) != 5:
        raise ValueError(f'보기 중복 발생: {cands} — 이 파라미터 조합은 문제로 성립 안 함')
    return tuple(sorted(cands))


def solve(prm):
    """보기 번호(1~5): 정답 a = d/b 가 보기 목록에서 차지하는 위치."""
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f'정답 {v} 이 보기 목록에 없음: {ch}')
    return ch.index(v) + 1


def _fmt(z):
    z = simplify(z)
    if z.is_integer:
        return str(z)
    if z.is_Rational:
        return f'{z.p}/{z.q}'
    return str(z)


def statement(prm):
    """해당 파라미터로 만들어지는 문제 문장 (한국어, 객관식)."""
    c, b, d = prm['c'], prm['b'], prm['d']
    ch = choices(prm)
    marks = '①②③④⑤'
    head = f'함수 f(x) = {c}/({b}x - {d}) + a의 정의역과 치역이 서로 같을 때, 상수 a의 값은? [3점]'
    body = '    '.join(f'{marks[i]} {_fmt(ch[i])}' for i in range(len(ch)))
    return head + '\n' + body


# 유사문제 재생성 예: (b, d) 를 바꾼, 문제로 성립하는 조합 2개
#   (b=5, d=21) → a = 21/5, 정답 ③  /  (b=2, d=9) → a = 9/2, 정답 ④
#   둘 다 원문제의 정답 ⑤ 와 다르다.
VARIANTS = [
    {'b': 5, 'd': 21},   # a = 21/5 → 정답 ③
    {'b': 2, 'd': 9},    # a = 9/2  → 정답 ④
]

# 원문제 보기 (3/2, 2, 5/2, 3, 7/2) 와 정답 ⑤ 고정 확인
_ORIG_CHOICES = (Rational(3, 2), 2, Rational(5, 2), 3, Rational(7, 2))
assert choices(PARAMS) == _ORIG_CHOICES, '유도 보기가 원문제 보기와 다름'
assert solve(PARAMS) == CANDIDATE, 'solve(PARAMS) 가 CANDIDATE 를 재현하지 못함'

if __name__ == '__main__':
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
