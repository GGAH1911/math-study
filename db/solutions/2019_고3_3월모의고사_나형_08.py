"""2019 고3 3월모의고사 나형 8번 — 파라미터화.

원문제: 자연수 x에 대한 명제
   'a ≤ x ≤ b 이면 x ≤ c 이다.'
가 거짓임을 보여 주는 x의 값을 5개의 보기 중에서 고르는 문제.

[수학 구조]
  p: a ≤ x ≤ b   (조건명제의 전건)
  q: x ≤ c        (조건명제의 후건)
  p → q 가 거짓 ⇔ p 는 참이고 q 는 거짓
                 ⇔ x ∈ [a, b] ∩ (c, ∞)         ... 이 교집합을 sympy Interval 로 직접 계산.
  보기(options) 중 이 교집합에 속하는 값이 정답이며, 그 값이 정렬된 보기 중 몇 번째(1-indexed)
  인지가 최종 답(선택형 정답 번호, CANDIDATE).

[파라미터로 뽑은 것]
  a, b : p(전건)의 하한/상한
  c    : q(후건)의 상한
  options : 제시되는 5개의 보기 값
  → a,b,c 는 서로 묶여 있어(반례가 보기 중 '유일'해야 문제가 성립) 하나만 자유로이
    못 흔들 수 있으므로 VARIANTS 로 유효 조합을 여러 개 제시한다.
  → options 는 (a,b,c)가 같아도 자유로이 바꿀 수 있고, 바뀌면 정답 번호가 실제로 달라진다.
"""
import sympy as sp

CANDIDATE = 4  # 원문제 정답: ④ (보기 4번째, 값 9)

PARAMS = dict(
    a=5,
    b=9,
    c=8,
    options=(6, 7, 8, 9, 10),
)

# (a,b,c)는 서로 묶인 파라미터(반례가 보기 중 유일해야 문제가 성립) → 유효 조합을 여러 개 제시.
# options 는 (a,b,c)와 독립적으로 바꿀 수 있는 파라미터.
VARIANTS = [
    dict(a=5, b=9, c=8, options=(6, 7, 8, 9, 10)),  # 원문제 그대로 → 답 4
    dict(a=5, b=9, c=8, options=(1, 2, 3, 4, 9)),   # options만 변경 → 답 5
    dict(a=5, b=8, c=7, options=(6, 7, 8, 9, 10)),  # a,b,c 이동(값 8이 정답) → 답 3
]


def _solve_counterexample_set(prm):
    """sympy Interval 로 p ∧ ¬q 의 해집합(구간)을 실제로 계산한다."""
    a, b, c = prm['a'], prm['b'], prm['c']
    p_interval = sp.Interval(a, b)              # p: a ≤ x ≤ b
    not_q_interval = sp.Interval.open(c, sp.oo)  # ¬q: x > c
    return p_interval.intersect(not_q_interval)  # p ∧ ¬q 의 해집합


def _counterexample(prm):
    """options 중 해집합에 속하는 값(반례)을 찾아 (값, 1-indexed 위치, 정렬된 보기) 반환."""
    options = prm['options']
    if len(set(options)) != len(options):
        raise ValueError("보기에 중복된 값이 있습니다.")
    sol_set = _solve_counterexample_set(prm)

    matches = [opt for opt in options if bool(sol_set.contains(sp.Integer(opt)))]
    if len(matches) != 1:
        raise ValueError(f"보기 중 반례가 유일하지 않습니다(문제로 성립하지 않음): {matches}")

    value_ = int(matches[0])
    sorted_opts = sorted(options)
    idx = sorted_opts.index(value_) + 1
    return value_, idx, sorted_opts


def value(prm):
    """수학적 답: 명제를 거짓으로 만드는 자연수 x."""
    v, _, _ = _counterexample(prm)
    return v


def choices(prm):
    """보기 목록: value()로 유도된 정답을 포함해 정렬된 5개 보기."""
    _, _, sorted_opts = _counterexample(prm)
    return tuple(sorted_opts)


def solve(prm):
    """보기 번호(1-indexed) — 객관식 정답."""
    _, idx, _ = _counterexample(prm)
    return idx


def statement(prm):
    a, b, c = prm['a'], prm['b'], prm['c']
    opts = choices(prm)
    circled = ['①', '②', '③', '④', '⑤']
    opts_str = ' '.join(f"{circled[i]} {v}" for i, v in enumerate(opts))
    return (
        "자연수 x에 대하여 명제\n"
        f"  '{a} \\le x \\le {b} 이면 x \\le {c} 이다.'\n"
        "  가 거짓임을 보여 주는 x의 값은?\n"
        f"  {opts_str}"
    )


# 원문제 보기(6,7,8,9,10)가 그대로 재현되는지 고정.
assert choices(PARAMS) == (6, 7, 8, 9, 10)
assert value(PARAMS) == 9

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')

if __name__ == '__main__':
    for prm in VARIANTS:
        print(prm, '-> 답:', solve(prm), '| 값:', value(prm))
        print(statement(prm))
        print()
