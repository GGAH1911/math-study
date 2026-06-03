import sympy as sp
k, x, a, b = sp.symbols('k x a b')

# 원래 방정식
eq = x**2 - 2*(k-a)*x + k**2 - 4*k + b

# 판별식이 k의 모든 값에 대해 0이 되는 조건
# 판별식 = 4(k-a)^2 - 4(k^2 - 4k + b)
discriminant = 4*(k-a)**2 - 4*(k**2 - 4*k + b)
discriminant_expanded = sp.expand(discriminant)
print(f'Discriminant: {discriminant_expanded}')

# k에 대해 정리
discriminant_poly = sp.Poly(discriminant_expanded, k)
coeffs = discriminant_poly.all_coeffs()
print(f'Coefficients [k, const]: {coeffs}')

# k의 계수가 0, 상수항이 0이어야 함
# -8*a + 16 = 0 => a = 2
# 4*a^2 - 4*b = 0 => b = a^2

a_val = 2
b_val = a_val**2

print(f'a = {a_val}, b = {b_val}')
print(f'a + b = {a_val + b_val}')

# 검증: a=2, b=4일 때 방정식이 완전제곱식인지 확인
eq_check = eq.subs([(a, a_val), (b, b_val)])
print(f'\nEquation with a={a_val}, b={b_val}: {eq_check}')
factored = sp.factor(eq_check)
print(f'Factored form: {factored}')

# 몇 가지 k값에서 판별식이 0인지 확인
for k_test in [0, 1, -1, 5]:
    d = eq_check.subs(k, k_test)
    disc = sp.discriminant(d, x)
    print(f'k={k_test}: discriminant = {disc}')

if all(eq_check.subs(k, k_test).subs(x, k_test - a_val) == 0 for k_test in [0, 1, -1, 2, 3]):
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')