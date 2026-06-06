from sympy import symbols, solve, simplify, Rational

CANDIDATE = '11'

# 원래 문제 정의
# 함수: f(x) = x^3 - 6x^2 + 5x
def f(x):
    return x**3 - 6*x**2 + 5*x

# 도함수: f'(x) = 3x^2 - 12x + 5
def f_prime(x):
    return 3*x**2 - 12*x + 5

# Step 1: 평균변화율 계산 (x가 0에서 4까지 변할 때)
# (f(4) - f(0)) / (4 - 0)
avg_rate = Rational(f(4) - f(0), 4)

# Step 2: 조건식 풀기: f'(a) = 평균변화율
# 3a^2 - 12a + 5 = avg_rate
a = symbols('a', real=True)
roots = solve(f_prime(a) - avg_rate, a)

# Step 3: 0 < a < 4 범위의 근만 필터링
valid_roots = [r for r in roots if r.is_real and 0 < float(r.evalf()) < 4]

# Step 4: 조건을 만족하는 모든 근의 곱 계산
product = 1
for root in valid_roots:
    product *= root
product = simplify(product)

# Step 5: 곱이 q/p 형태일 때 (p, q 서로소)
# product = 8/3 이므로 q = 8, p = 3
p = product.q  # denominator
q = product.p  # numerator

# Step 6: p + q 계산
answer = p + q

# Step 7: 원래 식으로 검증
if answer == int(CANDIDATE):
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")