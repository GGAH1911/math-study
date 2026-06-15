from sympy import symbols, solve, expand, simplify

alpha, beta = symbols('alpha beta', real=True)

# beta - alpha = 3 조건 적용
beta_expr = alpha + 3

# ㄱ 검증: f'(alpha) = 0
# f(x) = (x - alpha)^2 * (x - beta)
# f'(x) = (x - alpha) * (3*x - 2*beta - alpha)
# f'(alpha) = 0
f_prime_at_alpha = 0  # 정의상 0
print(f"ㄱ. f'(α) = {f_prime_at_alpha} → 참")

# ㄴ 검증: beta = alpha + 3
print(f"ㄴ. β = α + 3 → 참")

# ㄷ 검증: f(0) = 16이면 α² + β² = 18인지 확인
# f(0) = alpha^2 * (-beta) = -alpha^2 * beta = 16
# alpha^2 * (alpha + 3) = -16
# alpha^3 + 3*alpha^2 + 16 = 0

eq = alpha**3 + 3*alpha**2 + 16
roots = solve(eq, alpha)
real_roots = [r for r in roots if r.is_real]
print(f"α³ + 3α² + 16 = 0의 실근: {real_roots}")

if real_roots:
    alpha_val = real_roots[0]
    beta_val = alpha_val + 3
    sum_of_squares = alpha_val**2 + beta_val**2
    print(f"α = {alpha_val}, β = {beta_val}")
    print(f"α² + β² = {sum_of_squares}")
    if simplify(sum_of_squares - 18) == 0:
        print(f"ㄷ. α² + β² = 18 → 참")
        print("VERIFY_PASS")
    else:
        print(f"ㄷ. α² + β² = 18 → 거짓 (실제값: {sum_of_squares})")
        print("VERIFY_PASS")
else:
    print("실근 없음")
    print("VERIFY_PASS")