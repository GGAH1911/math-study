from sympy import Rational

CANDIDATE = 686

# 주어진 조건:
# 1. sum(a_n + a_{n+1}) = 5
# 2. sum(|a_{n+1}+a_{n+2}| * sin(nπ/2)) = 2

# 등비수열 {a_n}: a_n = a*r^(n-1), |r| < 1
# 조건 1: a(1+r)/(1-r) = 5
# 조건 2 (r < 0): a(1-|r|)*|r|/(1+r^2) = 2
# 풀이: r = -1/3, a = 10

a = Rational(10)
r = Rational(-1, 3)

# 원본 조건 1 검증
cond1_value = a * (1 + r) / (1 - r)
assert cond1_value == 5, f"Condition 1 failed: {cond1_value} != 5"

# 원본 조건 2 검증
abs_r = abs(r)
cond2_value = a * (1 - abs_r) * abs_r / (1 + r**2)
assert cond2_value == 2, f"Condition 2 failed: {cond2_value} != 2"

# 필요한 합 계산
sum_a_n = a / (1 - r)  # = 15/2
sum_a_3n = a * r**2 / (1 - r**3)  # = 15/14

# 문제에서 구하는 식
# sum_{n=1}^{∞} (100*a_n - m*a_{3n}) = 100*sum_a_n - m*sum_a_3n
# = 100*(15/2) - m*(15/14)
# = 750 - 15m/14

def evaluate_sum(m):
    return 100 * sum_a_n - m * sum_a_3n

# CANDIDATE 대입
m = CANDIDATE
result = evaluate_sum(m)

# 결과가 자연수인지 검증 (원본 문제 조건)
is_natural_at_candidate = (result > 0) and (result.denominator == 1)

# m이 최댓값임을 확인: m+1일 때는 자연수가 아님
m_next = m + 1
result_next = evaluate_sum(m_next)
is_natural_at_next = (result_next > 0) and (result_next.denominator == 1)

# 종합 검증
is_valid = is_natural_at_candidate and not is_natural_at_next

if is_valid:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")