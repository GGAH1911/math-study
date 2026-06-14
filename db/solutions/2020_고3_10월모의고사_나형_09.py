from sympy import binomial, Rational

# 문제 조건
# 동전을 6번 던져서 앞면이 2번 이상 나올 확률
n = 6  # 시행 횟수
p = Rational(1, 2)  # 앞면이 나올 확률

# 이항분포 P(X = k) = C(n, k) * p^k * (1-p)^(n-k)
def binomial_prob(n, k, p):
    return binomial(n, k) * p**k * (1 - p)**(n - k)

# 여사건을 이용: P(X >= 2) = 1 - P(X = 0) - P(X = 1)
prob_x_eq_0 = binomial_prob(n, 0, p)  # C(6,0) * (1/2)^6 = 1/64
prob_x_eq_1 = binomial_prob(n, 1, p)  # C(6,1) * (1/2)^6 = 6/64

# 원래 식으로 구한 답
CANDIDATE = 1 - (prob_x_eq_0 + prob_x_eq_1)

# 기대값
expected = Rational(57, 64)

# 조건 검증: 확률 범위 및 기대값 일치
if CANDIDATE == expected and 0 <= CANDIDATE <= 1:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")