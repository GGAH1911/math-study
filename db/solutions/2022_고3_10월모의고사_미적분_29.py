CANDIDATE = 20

from sympy import symbols, sin, cos, tan, limit

theta = symbols('theta', real=True, positive=True)

# 검증된 풀이에서 제시한 함수들
# f(θ) = θ + sin(2θ)cos(2θ)/(2cos(2θ) + 1)
f_theta = theta + sin(2*theta) * cos(2*theta) / (2*cos(2*theta) + 1)

# g(θ) = θ/2 - tan(θ)/(4(2cos(2θ) + 1))
g_theta = theta/2 - tan(theta) / (4 * (2*cos(2*theta) + 1))

# 문제 조건: lim_{θ→0+} S₁/S₂ = α
# 검증된 풀이에서 α = lim_{θ→0+} g(θ)/f(θ)
alpha = limit(g_theta / f_theta, theta, 0, '+')

# 최종 답: 80α
eighty_alpha = 80 * alpha

# 정답 확인 (CANDIDATE와 실제 계산값 비교)
if eighty_alpha == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")