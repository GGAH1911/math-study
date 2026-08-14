# -*- coding: utf-8 -*-
"""
[문제 구조]
최고차항의 계수가 1인 삼차함수 f(x)가
  (가) 방정식 f(x)=0의 실근은 alpha, beta (alpha<beta) 뿐
  (나) f(x)의 극솟값은 -m
을 만족한다.  (가)는 f(x) = (x-alpha)^2 * (x-beta) 형태(이중근)를 강제한다.

  f'(x) = (x-alpha)(3x - 2*beta - alpha)
  극소점 x = (2*beta+alpha)/3 에서의 극솟값 = -4*(beta-alpha)^3/27

이 값이 -m 이라는 (나)조건이 beta-alpha 간격(actual_d)을 유일하게 결정한다.

<보기>
  ㄱ. f'(alpha)=0                                    (구조상 항상 참 — 이중근이므로)
  ㄴ. beta = alpha + claimed_d                       (실제 간격 actual_d 와 비교해 참/거짓)
  ㄷ. f(0)=K 이면 alpha^2+beta^2 = claimed_sum 이다.  (f(0)=K 로 alpha를 유일하게 정한 뒤 비교)

파라미터화 포인트:
  - m          : (나) 조건에 등장하는 극솟값의 크기 (극솟값=-m)  → beta-alpha 간격을 결정
  - claimed_d  : 보기 ㄴ이 주장하는 beta-alpha 값               → ㄴ의 참/거짓을 바꿈
  - K          : ㄷ 조건에 등장하는 f(0) 값                      → alpha 값을 바꿈
  - claimed_sum: 보기 ㄷ이 주장하는 alpha^2+beta^2 값             → ㄷ의 참/거짓을 바꿈

즉 (m, K)는 문제 상황(삼차함수) 자체를 정의하고, (claimed_d, claimed_sum)은
<보기>가 내세우는 '주장값'이라 실제 계산값과 일치하는지 여부로 참/거짓이 갈린다.
ㄱ은 이중근 구조에서 나오는 항상-참 명제라 답이 될 수 있는 선택지는
{①, ②, ③, ⑤} 중 하나로 자동으로 좁혀진다(④ ㄴ,ㄷ은 ㄱ이 빠져 있어 논리상 나올 수 없음
— 실제 이 시험 문제 설계와 동일).
"""
from sympy import symbols, Eq, diff, simplify, Rational
from sympy import solve as sp_solve

x = symbols('x', real=True)

CANDIDATE = 2  # 원문제 정답: ② (ㄱ, ㄴ)

PARAMS = dict(
    m=Rational(4),             # (나) 조건: 극솟값 = -m
    claimed_d=Rational(3),     # 보기 ㄴ: beta = alpha + claimed_d
    K=Rational(16),            # ㄷ 조건: f(0) = K
    claimed_sum=Rational(18),  # 보기 ㄷ: alpha^2+beta^2 = claimed_sum (원문제 주장값, 실제로는 거짓)
)

# <보기> 문항 구성 방식 자체는 이 문제 형식에서 고정된 5개 조합 (원문제 보기와 동일함을 아래 assert로 고정)
CHOICE_SETS = [
    frozenset({'ㄱ'}),
    frozenset({'ㄱ', 'ㄴ'}),
    frozenset({'ㄱ', 'ㄷ'}),
    frozenset({'ㄴ', 'ㄷ'}),
    frozenset({'ㄱ', 'ㄴ', 'ㄷ'}),
]
assert CHOICE_SETS == [
    frozenset({'ㄱ'}), frozenset({'ㄱ', 'ㄴ'}), frozenset({'ㄱ', 'ㄷ'}),
    frozenset({'ㄴ', 'ㄷ'}), frozenset({'ㄱ', 'ㄴ', 'ㄷ'}),
]


def _actual_gap(m):
    """(나) 조건 극솟값=-m 으로부터 beta-alpha 간격(양의 실수)을 sympy로 실제로 푼다."""
    dd = symbols('dd', positive=True)
    sols = sp_solve(Eq(-Rational(4, 27) * dd**3, -m), dd)
    real_pos = [s for s in sols if s.is_real and s > 0]
    if len(real_pos) != 1:
        raise ValueError("극솟값 조건으로부터 beta-alpha 간격이 유일하게 정해지지 않습니다.")
    return real_pos[0]


def value(prm):
    """조건 (가)(나)(다)를 sympy로 실제로 풀어 ㄱ,ㄴ,ㄷ 각각의 참/거짓과
    실제 alpha, beta 값을 계산해 돌려준다."""
    m, claimed_d, K, claimed_sum = prm['m'], prm['claimed_d'], prm['K'], prm['claimed_sum']

    alpha, beta = symbols('alpha beta', real=True)
    f = (x - alpha)**2 * (x - beta)
    fprime = diff(f, x)

    # ㄱ: f'(alpha) = 0  (이중근 구조에서 항상 성립)
    truth_g = simplify(fprime.subs(x, alpha)) == 0

    # 실제 beta-alpha 간격
    actual_d = _actual_gap(m)

    # ㄴ: beta = alpha + claimed_d 가 실제 간격과 일치하는가
    truth_n = simplify(actual_d - claimed_d) == 0

    # ㄷ: f(0)=K 조건으로 alpha를 유일하게 결정 -> a^3 + actual_d*a^2 + K = 0
    aa = symbols('aa', real=True)
    cubic = aa**3 + actual_d * aa**2 + K
    roots = sp_solve(Eq(cubic, 0), aa)
    real_roots = [r for r in roots if r.is_real]
    if len(real_roots) != 1:
        raise ValueError("f(0)=K 조건을 만족하는 alpha가 유일하게 정해지지 않습니다.")
    alpha_val = real_roots[0]
    beta_val = alpha_val + actual_d
    actual_sum = simplify(alpha_val**2 + beta_val**2)

    truth_d = simplify(actual_sum - claimed_sum) == 0

    return dict(
        truth_g=truth_g, truth_n=truth_n, truth_d=truth_d,
        alpha=alpha_val, beta=beta_val, actual_d=actual_d, actual_sum=actual_sum,
    )


def choices(prm):
    return CHOICE_SETS


def solve(prm):
    v = value(prm)
    true_set = set()
    if v['truth_g']:
        true_set.add('ㄱ')
    if v['truth_n']:
        true_set.add('ㄴ')
    if v['truth_d']:
        true_set.add('ㄷ')
    for i, cs in enumerate(choices(prm)):
        if cs == true_set:
            return i + 1
    raise ValueError(f"참인 보기 조합 {true_set} 에 해당하는 선택지가 없습니다.")


def statement(prm):
    m, claimed_d, K, claimed_sum = prm['m'], prm['claimed_d'], prm['K'], prm['claimed_sum']
    return (
        "최고차항의 계수가 1인 삼차함수 f(x)가 다음 조건을 만족시킨다.\n"
        "(가) 방정식 f(x)=0의 실근은 \\alpha, \\beta (\\alpha < \\beta)뿐이다.\n"
        f"(나) 함수 f(x)의 극솟값은 -{m}이다.\n"
        "<보기>에서 옳은 것만을 있는 대로 고른 것은?\n"
        "ㄱ. f'(\\alpha)=0\n"
        f"ㄴ. \\beta=\\alpha+{claimed_d}\n"
        f"ㄷ. f(0)={K}이면 \\alpha^2+\\beta^2={claimed_sum}이다.\n"
        "① ㄱ ② ㄱ, ㄴ ③ ㄱ, ㄷ ④ ㄴ, ㄷ ⑤ ㄱ, ㄴ, ㄷ"
    )


if __name__ == '__main__':
    print(statement(PARAMS))
    v = value(PARAMS)
    print(f"ㄱ:{v['truth_g']} ㄴ:{v['truth_n']} ㄷ:{v['truth_d']}  "
          f"(alpha={v['alpha']}, beta={v['beta']}, alpha^2+beta^2={v['actual_sum']})")
    ans = solve(PARAMS)
    print('선택지 번호:', ans)
    print('VERIFY_PASS' if ans == CANDIDATE else 'VERIFY_FAIL')
