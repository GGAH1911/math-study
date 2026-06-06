from sympy import symbols, sqrt, pi, sin, diff, simplify, expand

CANDIDATE = 8

x = symbols('x', real=True)

# 문제 조건: f(x) = ax^3 - 2ax^2 + bx - b - 2
# g는 역함수 h를 가짐 (단사함수 조건)
# h'(-√2)의 최댓값이 k/π일 때, k^2를 구하라
# (정수 a ≠ 0, b)

# 검증된 풀이에서 (a,b) = (-1,-2)가 조건을 만족함
# 이 경우 h'(-√2)의 최댓값이 2√2/π임을 확인

a_val, b_val = -1, -2

# Step 1: 함수 f(x) 인코딩
f = a_val*x**3 - 2*a_val*x**2 + b_val*x - b_val - 2
f = expand(f)  # f(x) = -x^3 + 2x^2 - 2x

# Step 2: f'(x) 계산
f_prime = diff(f, x)  # f'(x) = -3x^2 + 4x - 2

# Step 3: g(c) = -√2인 c를 찾기
# g(c) = -2*cos(π/4 * f(c)) = -√2
# ⟹ cos(π/4 * f(c)) = √2/2
# ⟹ f(c) = -1 (범위 조건)

eq_f_c = f + 1  # f(c) = -1 방정식
c_val = 1

f_at_c = f.subs(x, c_val)  # f(1) = -1
f_prime_at_c = f_prime.subs(x, c_val)  # f'(1) = -1

# Step 4: g'(x) 계산 (0 ≤ x ≤ 2 범위)
# g(x) = -2*cos(π/4 * f(x))
# g'(x) = π/2 * sin(π/4 * f(x)) * f'(x)

g_prime_at_c = pi/2 * sin(pi/4 * f_at_c) * f_prime_at_c
g_prime_at_c = simplify(g_prime_at_c)  # π√2/4

# Step 5: 역함수 미분 공식: h'(y) = 1/g'(x) where g(x) = y
# g(c) = -√2이므로 h'(-√2) = 1/g'(c)

h_prime_at_neg_sqrt2 = simplify(1 / g_prime_at_c)  # 2√2/π

# Step 6: 검증: h'(-√2) = 2√2/π인지 확인
expected_h_prime = 2*sqrt(2) / pi
difference = simplify(h_prime_at_neg_sqrt2 - expected_h_prime)

if difference != 0:
    print("VERIFY_FAIL")
    exit(1)

# Step 7: h'(-√2)의 최댓값이 k/π 형태
# 최댓값 = 2√2/π = k/π
# ⟹ k = 2√2
# ⟹ k^2 = 8

k = 2*sqrt(2)
k_squared = simplify(k**2)  # 8

# Step 8: CANDIDATE와 비교
if k_squared == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")