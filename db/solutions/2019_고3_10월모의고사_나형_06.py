# -*- coding: utf-8 -*-
"""
원문제 (2026-08-14 기준):
  ∫_{-3}^{3} (x^3 + 4x^2) dx + ∫_{3}^{-3} (x^3 + x^2) dx 의 값은?
  ① 36 ② 42 ③ 48 ④ 54 ⑤ 60      [정답] ④(=4)

수학 구조
  - x^3 항은 기함수이므로 대칭구간 [-a, a] 위 적분은 항상 0.
  - 짝함수 c*x^2 항의 대칭구간 적분은  c * (2a^3/3).
  - 두 번째 적분은 상한/하한이 뒤바뀌어 있으므로 부호가 반전된다.
  즉  값 = c1*(2a^3/3) - c2*(2a^3/3) = (c1 - c2) * (2a^3/3)

파라미터화
  a  : 적분 구간의 반경 [-a, a]  (원문제 3)
  c1 : 첫 번째 적분의 x^2 계수   (원문제 4)
  c2 : 두 번째 적분의 x^2 계수   (원문제 1)
  세 값 모두 실제로 답(값 자체 및 5지선다 중 몇 번인지)을 바꾼다 — 아래 VARIANT 검증 참고.

보기(선택지) 생성 구조
  원문제의 보기 36,42,48,54,60 은 공차 d=2a(=6)의 등차수열이며,
  정답(54)은 정수 m = value/d = (c1-c2)*a^2/3 에 대해 window 안에서
  index = (m-1) mod 5 위치에 온다 (m=9 → index=3 → 4번째 보기, 즉 ④).
  이 규칙 자체는 값(value)에서 유도되므로 파라미터가 바뀌면 정답이 놓이는
  '몇 번째 보기인지'도 함께 바뀐다 (아래에서 c1, a 각각 단독으로 바꿔도
  선택 번호가 달라짐을 직접 확인했다).
"""

from sympy import symbols, integrate, Rational

CANDIDATE = 4  # ★원문제 정답(보기 번호, ④) — 절대 바꾸지 않음

PARAMS = dict(
    a=3,   # 적분 구간 [-a, a]
    c1=4,  # 첫 번째 피적분함수의 x^2 계수
    c2=1,  # 두 번째 피적분함수의 x^2 계수
)


def value(prm):
    """실제 수학적 답: sympy로 두 정적분을 계산해 합산."""
    a, c1, c2 = prm["a"], prm["c1"], prm["c2"]
    x = symbols("x")
    f1 = x ** 3 + c1 * x ** 2
    f2 = x ** 3 + c2 * x ** 2
    result1 = integrate(f1, (x, -a, a))
    result2 = integrate(f2, (x, a, -a))  # 상한 a, 하한 -a로 뒤바뀐 두 번째 적분
    return result1 + result2


def choices(prm):
    """
    value(prm)에서 유도한 5지선다 보기.
    공차 d = 2a 인 등차수열(정수 그리드) 위에서, 정답이 놓일 위치를
    m = value/d 의 값에서 파생된 index = (m-1) mod 5 로 정한다.
    m이 정수가 아니면(=격자에 안 맞으면) 성립하지 않는 문제이므로 예외를 던진다.
    """
    a, c1, c2 = prm["a"], prm["c1"], prm["c2"]
    v = value(prm)
    d = 2 * a
    if d == 0:
        raise ValueError("a=0이면 적분 구간이 소멸해 문제가 성립하지 않습니다.")

    m_rat = Rational(v, d)
    if m_rat.q != 1:
        raise ValueError(f"value={v}가 공차 d={d}의 정수 격자 위에 놓이지 않습니다.")
    m = int(m_rat)

    index = (m - 1) % 5  # value로부터 유도된, 정답이 위치할 0-based 인덱스
    start = m - index
    grid = [(start + k) * d for k in range(5)]

    if grid[index] != v:
        raise ValueError("보기 생성 로직 불일치")

    return grid


def solve(prm):
    """조건 -> 보기 번호(1~5)."""
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f"value={v}가 생성된 보기 {ch} 안에 없습니다.")
    return ch.index(v) + 1


def statement(prm):
    a, c1, c2 = prm["a"], prm["c1"], prm["c2"]
    ch = choices(prm)
    circled = ["①", "②", "③", "④", "⑤"]
    opts = " ".join(f"{circled[i]} {ch[i]}" for i in range(5))
    def term(c):
        coef = "" if abs(c) == 1 else str(abs(c))
        return f"+ {coef}x^{{2}}" if c >= 0 else f"- {coef}x^{{2}}"

    c1_term = term(c1)
    c2_term = term(c2)
    return (
        f"\\int_{{-{a}}}^{{{a}}}(x^{{3}}{c1_term})dx"
        f"+\\int_{{{a}}}^{{-{a}}}(x^{{3}}{c2_term})dx 의 값은?\n"
        f"{opts}"
    )


# --- 원문제 보기(36,42,48,54,60)가 그대로 재현되는지 고정 ---
assert choices(PARAMS) == [36, 42, 48, 54, 60], choices(PARAMS)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')

if __name__ == "__main__":
    # 파라미터를 하나씩 바꿔 정답(보기 번호)이 실제로 달라지는지 확인
    variants = [
        dict(PARAMS, c1=7),       # c1-c2: 3 -> 6
        dict(PARAMS, c2=2),       # c1-c2: 3 -> 2
        dict(a=6, c1=4, c2=1),    # a: 3 -> 6 (3의 배수 유지)
    ]
    print("원문제:", statement(PARAMS), "->", solve(PARAMS))
    for v in variants:
        print(v, "-> value=", value(v), " choices=", choices(v), " answer=", solve(v))
