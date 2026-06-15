import math
from sympy import symbols, Eq, solve

CANDIDATE = 1

# 선택지
answers = [0.5328, 0.6247, 0.7745, 0.8185, 0.9104]
expected = answers[CANDIDATE - 1]

# 핵심 1: 조건 f(12) <= g(20)에서 (20-m)^2 <= 4
# X,Y 모두 표준편차 2이므로 밀도함수 계수 동일
# f(12) = (1/(2√(2π))) * exp(-1/2)
# g(20) = (1/(2√(2π))) * exp(-(20-m)^2/8)
# f(12) <= g(20) => -1/2 <= -(20-m)^2/8 => (20-m)^2 <= 4

m = symbols('m', real=True)
m_range = sorted(solve(Eq((20 - m)**2, 4), m))  # [18, 22]

# 핵심 2: 범위 [18, 22]에서 P(21 <= Y <= 24)를 최대화하는 m=22
# 구간 [21, 24]의 중점 22.5에 가까울수록 확률 최대 => m <= 22이므로 m=22
m_opt = 22
assert m_range[0] <= m_opt <= m_range[1], f"m={m_opt}가 범위 {m_range} 밖"
assert (20 - m_opt)**2 <= 4, "조건 불만족"

# 핵심 3: m=22일 때 P(21 <= Y <= 24)
# 표준화: Z = (Y-22)/2 ~ N(0,1)
# P(21 <= Y <= 24) = P((21-22)/2 <= Z <= (24-22)/2)
#                  = P(-0.5 <= Z <= 1)
# 대칭성 이용: P(-0.5 <= Z <= 1) = P(0 <= Z <= 0.5) + P(0 <= Z <= 1)
#                                 = 0.1915 + 0.3413

prob_max = 0.1915 + 0.3413

# 검증
assert math.isclose(prob_max, expected, rel_tol=1e-9), \
    f"계산값 {prob_max}이 예상값 {expected}와 불일치"

print("VERIFY_PASS")