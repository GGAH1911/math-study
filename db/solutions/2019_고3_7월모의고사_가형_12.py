from sympy import symbols, Function, diff, limit

# 조건 검증
f_1 = 2
f_prime_1 = 3
h_1 = 5
h_prime_1 = 12

# 연쇄법칙으로부터
# h'(1) = g'(f(1)) * f'(1) = g'(2) * 3 = 12
g_prime_2 = h_prime_1 / f_prime_1
assert g_prime_2 == 4, f'Expected g\'(2)=4, got {g_prime_2}'

# h(1) = g(f(1)) = g(2) = 5
g_2 = h_1
assert g_2 == 5, f'Expected g(2)=5, got {g_2}'

result = g_2 + g_prime_2
assert result == 9, f'Expected 9, got {result}'

print('VERIFY_PASS')