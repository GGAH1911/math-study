import cmath

# 주어진 방정식의 계수
a, b = 4, 13

# 세 근 구하기
alpha = 1
# beta, gamma는 x^2 + 4x + 13 = 0의 근
discriminant = a**2 - 4*b
beta = (-a + cmath.sqrt(discriminant)) / 2
gamma = (-a - cmath.sqrt(discriminant)) / 2

# 조건 확인: (2*alpha + 2*beta - gamma)^2 = -81
condition_value = (2*alpha + 2*beta - gamma)**2
print(f'Condition: (2α + 2β - γ)² = {condition_value}')
print(f'Expected: -81')
assert abs(condition_value - (-81)) < 1e-10, f'Condition failed: {condition_value}'

# 답 계산: (4+alpha)(4+beta)(4+gamma)
answer = (4 + alpha) * (4 + beta) * (4 + gamma)
print(f'(4+α)(4+β)(4+γ) = {answer}')
print(f'Real part: {answer.real}')
print(f'Imaginary part: {abs(answer.imag)}')

if abs(answer.imag) < 1e-10 and abs(answer.real - 65) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')