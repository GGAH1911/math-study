"""2019 고3 4월모의고사 나형 6번 — 파라미터 솔버.

문제: lim_{n→∞} (a + p^n) / (D + q^n) = T 일 때 상수 a 의 값은? (객관식 5지선다)

[수학 구조]
  |p| < 1, |q| < 1 이면 n→∞ 일 때 p^n → 0, q^n → 0 이므로
    lim = (a + 0) / (D + 0) = a / D = T   =>   a = T * D
  즉 정답값 a 는 (극한값 T) x (분모 상수항 D) 로 결정된다 — 이를 sympy 로
  기호 극한(sp.limit)과 방정식(sp.solve)을 실제로 풀어서 구한다.

[보기(선택지) 구조]
  원문제는 ①11 ②12 ③13 ④14 ⑤15 로, anchor(=11)부터 시작하는 연속된 정수 5개이다.
  anchor 는 "보기의 시작값"을 정하는 출제 파라미터로 별도로 둔다.
  정답 a 가 [anchor, anchor+4] 범위를 벗어나는 파라미터 조합(예: T나 D를 크게 바꾼
  경우)도 하나의 유사문제로 인정하기 위해, 보기 번호는 (a-anchor) mod 5 + 1 로
  순환 배치한다 — 범위 안에 있을 때는 이것이 곧 "몇 번째 보기인가"와 정확히 같다.

[답을 바꾸는 파라미터]
  - denom_const(D): a=T*D 자체를 바꾸고, anchor 대비 위치(mod 5)도 함께 바뀐다 → 보기 번호가 실제로 바뀜.
  - anchor: 보기의 시작값을 바꾸므로 같은 a 라도 몇 번째 보기인지가 바뀜.
  (target(T)은 a 값 자체는 바꾸지만 D=denom_const 가 5(=보기 개수)의 배수라서
   이 예제 파라미터에서는 mod 5 위치가 우연히 불변 — 그래도 value() 로 실제 정답이
   달라지는 것은 sympy 계산으로 확인 가능하다.)
"""
import sympy as sp

CANDIDATE = 5  # ★원문제 정답 — 보기 ⑤ (a=15). 절대 변경 금지

PARAMS = dict(
    base1=sp.Rational(1, 4),  # 분자 지수항의 밑 p  (|p|<1 이어야 p^n -> 0)
    base2=sp.Rational(1, 2),  # 분모 지수항의 밑 q  (|q|<1 이어야 q^n -> 0)
    denom_const=5,            # 분모의 상수항 D
    target=3,                 # 주어진 극한값 T
    anchor=11,                # 보기(①)의 시작값
)


def value(prm):
    """a 의 실제 값을 sympy 로 극한을 취하고 방정식을 풀어서 구한다."""
    b1 = sp.nsimplify(prm['base1'])
    b2 = sp.nsimplify(prm['base2'])
    if not (sp.Abs(b1) < 1) or not (sp.Abs(b2) < 1):
        raise ValueError('|밑| < 1 이 아니면 지수항이 0으로 수렴하지 않아 문제가 성립하지 않음')

    n = sp.symbols('n', positive=True, integer=True)
    a = sp.symbols('a')
    D = sp.nsimplify(prm['denom_const'])
    T = sp.nsimplify(prm['target'])

    f = (a + b1 ** n) / (D + b2 ** n)
    lim_expr = sp.limit(f, n, sp.oo)

    sols = sp.solve(sp.Eq(lim_expr, T), a)
    if len(sols) != 1:
        raise ValueError(f'a 에 대한 해가 유일하게 정해지지 않음: {sols}')
    v = sp.nsimplify(sols[0])
    if not v.is_number or v.has(sp.zoo, sp.nan, sp.oo, sp.I):
        raise ValueError(f'유효하지 않은 답: {v}')
    return v


def choices(prm):
    """anchor 부터 시작하는 연속된 정수 5개 (원문제 보기: ①11 ②12 ③13 ④14 ⑤15)."""
    anchor = sp.Integer(prm['anchor'])
    return [anchor + i for i in range(5)]


def solve(prm):
    """보기 번호(①=1 ... ⑤=5)를 반환한다.

    a 가 [anchor, anchor+4] 안에 있으면 그 위치가 곧 보기 번호이고, 파라미터를
    바꿔 a 가 이 범위를 벗어나더라도 (a-anchor) mod 5 로 같은 5지선다 틀에 순환
    배치해 문제가 계속 성립하도록 한다.
    """
    v = value(prm)
    if not v.is_integer:
        raise ValueError(f'a 가 정수가 아니어서 보기(정수) 문제로 성립하지 않음: {v}')
    anchor = sp.Integer(prm['anchor'])
    pos = int((v - anchor) % 5) + 1
    return pos


def statement(prm):
    b1, b2 = prm['base1'], prm['base2']
    D, T = prm['denom_const'], prm['target']
    ch = choices(prm)
    labels = '①②③④⑤'
    opts = ' '.join(f'{labels[i]} {c}' for i, c in enumerate(ch))
    return (
        f"lim_{{n→∞}} (a + ({sp.nsimplify(b1)})^n) / ({D} + ({sp.nsimplify(b2)})^n) = {T} 일 때, "
        f"상수 a의 값은?\n{opts}"
    )


# 원문제 파라미터로 만든 보기가 실제 원문제 보기 [11,12,13,14,15] 와 같은지 고정 검증
assert choices(PARAMS) == [11, 12, 13, 14, 15]
assert value(PARAMS) == 15

if __name__ == '__main__':
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
