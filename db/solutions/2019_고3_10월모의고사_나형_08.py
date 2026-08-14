# -*- coding: utf-8 -*-
"""
원문제: "m ≤ 135, n ≤ 9인 두 자연수 m, n에 대하여 ∛(2m) × √(n³)의 값이
자연수일 때, m+n의 최댓값은?" → 정답 ⑤ 117

파라미터화 규격:
  PARAMS = dict(a, M, N)
    a : 세제곱근 안의 계수  (원문제: 2)
    M : m 의 상한           (원문제: 135)
    N : n 의 상한           (원문제: 9)
  value(prm)     → 수학적 답 (m+n 의 최댓값)
  choices(prm)   → 보기 목록 (값에서 유도 + 파라미터에 따른 순서 회전)
  solve(prm)     → 보기 번호 (1~5)
  statement(prm) → 파라미터로 생성한 한국어 문제 문장

수학 구조 (sympy 로 실제 계산):
  √(n³) = n·√n 이므로 곱 ∛(a·m)·√(n³) 이 자연수가 되려면 n 은 완전제곱수여야
  한다 (∛(a·m) 은 3차 무리수, √n 은 2차 무리수 — 곱이 유리수가 되려면 √n ∈ ℚ).
  n = s² 이면 √(n³) = s³ 이고
      곱 = s³·(a·m)^(1/3) ∈ ℕ  ⟺  a·m·s⁹ 가 완전세제곱수.
  a·s⁹ = ∏ p^{e_p} 로 소인수분해하면 m = r·t³ (r = ∏ p^{(3 - e_p mod 3) mod 3})
  형태일 때만 성립하므로, 각 s 에 대한 최대 m 은
      r · ⌊(M//r)^(1/3)⌋³  (sympy integer_nthroot 로 정확 계산)
  이고 s² + m 의 최댓값이 답이다.

파라미터로 뽑은 수학 구조 (셋 다 독립적으로 움직이고 각각 답을 바꾼다):
  1. 세제곱근 계수 a — 완전세제곱 조건의 소인수 지수 구조를 바꾼다
  2. m 의 상한 M     — 최대 m 을 결정하는 바닥함수 경계를 바꾼다
  3. n 의 상한 N     — 허용되는 완전제곱수 n 의 범위를 바꾼다

보기 구조:
  정답 v 로부터 v-20, v-15, v-10, v-5, v 를 유도하고, 파라미터가 원문제에서
  벗어난 정도 (a-2)+(M-135)+(N-9) (mod 5) 만큼 회전시켜 정답 위치가 바뀌게
  한다. 원문제 파라미터에서는 회전 0 → [97, 102, 107, 112, 117] 이므로
  원문제 보기와 정확히 일치함을 assert 로 고정한다.
"""

from sympy import cbrt, factorint, integer_nthroot, simplify, sqrt


def _validate(prm):
    """파라미터가 자연수 조건(a, M, N 모두 1 이상의 정수)을 만족하는지 검사."""
    a = prm.get('a')
    M = prm.get('M')
    N = prm.get('N')
    for name, x in (('a', a), ('M', M), ('N', N)):
        if not isinstance(x, int) or x < 1:
            raise ValueError(f'{name} 은(는) 1 이상의 정수여야 한다: {x!r}')
    return a, M, N


def _max_m_for_s(a, M, s):
    """n = s² 일 때 곱이 자연수가 되는 최대 m(≤ M) 을 구한다.

    a·s⁹·m 이 완전세제곱수가 되어야 하므로 m = r·t³ 꼴.
    r 은 a·s⁹ 의 소인수분해(sympy factorint) 지수를 3의 배수로 끌어올리는
    최소 승수, t 의 최댓값은 sympy integer_nthroot 로 정확히 계산한다.
    성립하는 m 이 없으면 None.
    """
    r = 1
    for p, e in factorint(a * s**9).items():
        r *= p ** ((3 - e % 3) % 3)
    t = integer_nthroot(M // r, 3)[0]
    if t == 0:
        return None
    m = r * t**3
    # 방어 검증: a·m·s⁹ 가 완전세제곱수(곱이 자연수)인지
    assert integer_nthroot(a * m * s**9, 3)[1], \
        f'완전세제곱 조건 위반: a={a}, m={m}, s={s}'
    return m


def _verify_symbolic(a, m, n):
    """∛(a·m) × √(n³) 이 정수인지 sympy 기호로 검증한다."""
    prod = simplify(sqrt(n**3) * cbrt(a * m))
    return prod.is_integer is True


def value(prm):
    """수학적 답: 조건을 만족하는 (m, n) 에서 m+n 의 최댓값."""
    a, M, N = _validate(prm)
    best = None
    best_s = None
    s = 1
    while s * s <= N:  # n = s² (완전제곱수) 만 후보
        m = _max_m_for_s(a, M, s)
        if m is not None:
            total = m + s * s
            if best is None or total > best:
                best, best_s = total, s
        s += 1
    if best is None:
        raise ValueError(
            f'조건을 만족하는 (m, n) 이 없다: a={a}, M={M}, N={N}')
    # 최종 후보에 대한 기호 검증
    m_best = _max_m_for_s(a, M, best_s)
    assert _verify_symbolic(a, m_best, best_s * best_s), \
        f'기호 검증 실패: a={a}, m={m_best}, n={best_s * best_s}'
    return best


def choices(prm):
    """보기 목록: 정답 v 에서 v-20, v-15, v-10, v-5, v 를 유도.

    파라미터가 원문제에서 벗어난 정도만큼 회전시켜 정답 위치가 파라미터에
    따라 달라진다. (원문제 파라미터면 회전 0 → 원문제 보기 그대로)
    """
    a, M, N = _validate(prm)
    v = value(prm)
    base = [v - 20, v - 15, v - 10, v - 5, v]
    if len(set(base)) != 5 or any(c <= 0 for c in base):
        raise ValueError(f'유효한 보기를 만들 수 없다: v={v}')
    rot = ((a - 2) + (M - 135) + (N - 9)) % 5
    return base[rot:] + base[:rot]


def solve(prm):
    """보기 번호(1~5): choices 목록에서 정답 v 가 놓인 위치."""
    cs = choices(prm)
    return cs.index(value(prm)) + 1


def statement(prm):
    """파라미터로 생성한 한국어 문제 문장 (보기 포함)."""
    a, M, N = _validate(prm)
    marks = ['①', '②', '③', '④', '⑤']
    body = (f'm ≤ {M}, n ≤ {N}인 두 자연수 m, n에 대하여 '
            f'∛({a}m) × √(n³)의 값이 자연수일 때, m+n의 최댓값은? [3점]')
    opts = '  '.join(f'{mk} {c}' for mk, c in zip(marks, choices(prm)))
    return body + '\n' + opts


# =====================================================================
# 원문제 정의
# =====================================================================
CANDIDATE = 5                       # ★ 원문제 정답(보기 ⑤ 117) — 절대 변경 금지
PARAMS = dict(a=2, M=135, N=9)      # 원문제의 계수·상한

# ★ 유도한 보기가 원문제 보기와 같은지 고정 (값 117 → 97, 102, 107, 112, 117)
assert choices(PARAMS) == [97, 102, 107, 112, 117], \
    f'원문제 보기와 불일치: {choices(PARAMS)}'

# ★ 파라미터 하나씩 흔들어 답(보기 번호)이 실제로 바뀌는지 직접 확인
#   (a: 계수, M: m 의 상한, N: n 의 상한 — 전부 살아 있는 손잡이)
for _key, _nv in (('a', 3), ('M', 136), ('N', 10)):
    assert solve({**PARAMS, _key: _nv}) != CANDIDATE, \
        f'파라미터 {_key} 는 답을 바꾸지 못한다 (장식 파라미터)'

if __name__ == '__main__':
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
