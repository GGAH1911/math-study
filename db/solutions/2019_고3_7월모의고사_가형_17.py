import sympy as sp

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# 길이 L인 선분 AB를 지름으로 하는 반원(반지름 r=L/2), 그 위의 점 Q=(r cosα, r sinα),
# 지름 위의 점 P에 대해 QB=QP 조건을 걸면 원래 풀이의 벡터 내적 트릭에 의해
# ∠BQP = θ 일 때 정확히 α = θ 가 성립한다(등변삼각형 QPB의 밑각이 같아지는 구조).
# 이때 삼각형 QPB의 넓이는 S(θ) = r^2 · sinθ(1-cosθ) 이고, sinθ~θ, 1-cosθ~θ²/2
# (테일러 전개)로부터 S(θ) ~ (r²/2)θ³ 이 된다.
#
# 답을 실제로 바꾸는 두 파라미터:
#   L : AB의 길이(반지름 r=L/2를 결정) → 계수 r²=L²/4 로 값에 직접 반영
#   n : lim_{θ→0+} S(θ)ⁿ/θ^{3n} 의 거듭제곱 차수(n=1이면 원문제 그대로) →
#       극한값이 (r²/2)ⁿ 로 n제곱만큼 그대로 반영
# 두 값 모두 sympy limit() 으로 실제 계산하며 하드코딩된 숫자를 반환하지 않는다.
#
# 이 문제 유형은 보기가 "정답을 중심으로 한 2의 거듭제곱 수열"
# (①1/4 ②1/2 ③1 ④2 ⑤4)로 고정되어 나온다. 파라미터를 바꿔 계산된 값이
# 이 다섯 값 중 하나가 아니면 더 이상 "이 유형"의 문제로 성립하지 않으므로 예외를 던진다.

CANDIDATE = 2  # ★원문제 정답 (② 1/2, 즉 보기 번호 2)

PARAMS = dict(
    L=2,  # 선분 AB의 길이 (반지름 r = L/2)
    n=1,  # lim S(θ)^n / θ^{3n} 의 거듭제곱 차수 (n=1이면 원문제)
)


def value(prm):
    """조건을 만족하는 lim_{θ→0+} S(θ)^n/θ^{3n} 을 sympy 로 실제 계산."""
    L = prm['L']
    n = prm['n']
    if L <= 0 or n <= 0 or int(n) != n:
        raise ValueError("L>0, n은 양의 정수여야 문제가 성립한다")
    theta = sp.symbols('theta', positive=True)
    r = sp.Rational(L, 1) / 2
    # 등변삼각형(QB=QP) 구조에서 유도되는 넓이 S(θ) = r^2 * sinθ * (1-cosθ)
    S = r**2 * sp.sin(theta) * (1 - sp.cos(theta))
    T = S**n
    val = sp.limit(T / theta**(3 * n), theta, 0, '+')
    return val


def choices(prm):
    """이 문제 유형이 강제하는 고정 보기: 1/2을 중심으로 한 2의 거듭제곱 5개."""
    return (sp.Rational(1, 4), sp.Rational(1, 2), sp.Integer(1), sp.Integer(2), sp.Integer(4))


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f"값 {v}이(가) 보기 범위 {ch}를 벗어남 — 문제로 성립하지 않음")
    return ch.index(v) + 1  # 1-based 보기 번호 (①=1, ..., ⑤=5)


def statement(prm):
    L, n = prm['L'], prm['n']
    if n == 1:
        power_txt = r"\frac{S(\theta)}{\theta^3}"
    else:
        power_txt = r"\frac{\{S(\theta)\}^{%d}}{\theta^{%d}}" % (n, 3 * n)
    return (
        f"그림과 같이 길이가 {L}인 선분 AB를 지름으로 하는 반원이 있다. "
        r"선분 AB 위의 점 P에 대하여 \overline{QB} = \overline{QP} 를 만족시키는 "
        r"반원 위의 점을 Q라 할 때, \angle BQP = \theta \left( 0 < \theta < \frac{\pi}{2} \right) "
        r"라 하자. 삼각형 QPB의 넓이를 S(\theta)라 할 때, "
        rf"\lim_{{\theta \to 0+}} {power_txt} 의 값은?"
    )


# 원문제 보기가 정확히 ①1/4 ②1/2 ③1 ④2 ⑤4 인지 고정 검증
assert choices(PARAMS) == (sp.Rational(1, 4), sp.Rational(1, 2), 1, 2, 4)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
