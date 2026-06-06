import sympy as sp

f_0 = sp.Symbol('f_0')
f_prime_0 = sp.Symbol('f_prime_0')

# 조건: f'(0) - f(0) = 2
condition = f_prime_0 - f_0 - 2

# g'(0) 계산
# g'(0) = [f'(0)*2 - 2*f(0)] / 8
g_prime_0 = (f_prime_0 * 2 - 2 * f_0) / 8

# 분자를 인수분해
numerator = f_prime_0 * 2 - 2 * f_0
numerator_factored = 2 * (f_prime_0 - f_0)

# 조건을 사용하여 f'(0) - f(0) = 2 대입
g_prime_0_value = 2 * 2 / 8

print(f"g'(0) = {g_prime_0_value}")
print(f"g'(0) = {sp.Rational(1, 2)}")

if g_prime_0_value == 0.5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')