from sympy import *

# ─────────────────────────────────────────────────────────────
# 문제: lim_{x→0} (e^{5x}-1)/(3x) 의 값을 고르는 5지선다.
#
# 수학 구조:
#   극한값 v = a/b  (지수 계수 a, 분모 계수 b) — 로피탈/e^{ax}-1~ax 근사로 v=a/b
#   보기는 v를 정수 c(=반올림한 v)를 중심으로 폭 step=1/b 간격의
#   등차수열 5개로 구성된다: {c-2s, c-s, c, c+s, c+2s}.
#   (원문제의 보기 4/3,5/3,2,7/3,8/3 이 실제로 이 규칙을 따름: c=2, s=1/3)
#   정답 번호는 v가 이 보기들 중 몇 번째인지로 결정된다.
#
# 파라미터화되는 값: a(지수 계수), b(분모 계수/보기 간격의 역수)
#   → 각각 단독으로 바꿔도 v와 그에 따른 정답 번호가 실제로 달라짐(아래 검증).
# ─────────────────────────────────────────────────────────────

CANDIDATE = 2  # ★원문제 정답(②) — 절대 바꾸지 않음

PARAMS = dict(a=5, b=3)


def value(prm):
    """lim_{x->0} (e^{a x} - 1) / (b x) 를 sympy로 실제 계산."""
    x = symbols('x')
    a, b = prm['a'], prm['b']
    f = (exp(a * x) - 1) / (b * x)
    return limit(f, x, 0)


def choices(prm):
    """정답 v를 중심 c(=v를 반올림한 정수) 주변에 간격 1/b로 배치한 5개 보기."""
    b = prm['b']
    v = value(prm)
    c = round(v)  # sympy Rational에 대한 정수 반올림 (float 미사용)
    step = Rational(1, b)
    return (c - 2 * step, c - step, c, c + step, c + 2 * step)


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f"파라미터 조합 {prm} 은 유효한 5지선다 문제를 만들지 못함 (값 {v} 이 보기 밖)")
    return ch.index(v) + 1  # 1-based 보기 번호(①=1, ..., ⑤=5)


def statement(prm):
    a, b = prm['a'], prm['b']
    ch = choices(prm)
    circled = ['①', '②', '③', '④', '⑤']
    opts = '  '.join(f'{circled[i]} {ch[i]}' for i in range(5))
    return (
        f"lim_{{x→0}} (e^{{{a}x}}-1)/({b}x) 의 값은?\n"
        f"{opts}"
    )


# 원문제 보기 재현 확인
assert choices(PARAMS) == (Rational(4, 3), Rational(5, 3), 2, Rational(7, 3), Rational(8, 3))

if __name__ == '__main__':
    print(statement(PARAMS))
    print(f'극한값: {value(PARAMS)}, 정답 번호: {solve(PARAMS)}')

    # 파라미터 a, b 가 각각 단독으로 정답을 바꾸는지 검증
    variant_a = dict(PARAMS, a=7)   # v=7/3 → 다른 보기 index
    variant_b = dict(PARAMS, b=5)   # v=1  → 다른 보기 index
    print('a=7,b=3 ->', solve(variant_a), '(원래 2와 달라야 함)')
    print('a=5,b=5 ->', solve(variant_b), '(원래 2와 달라야 함)')
    assert solve(variant_a) != CANDIDATE
    assert solve(variant_b) != CANDIDATE

    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
