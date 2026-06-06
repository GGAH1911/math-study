import numpy as np
from scipy import integrate

# 값 설정
a = 2
b = 1/2
c = np.sqrt(2)

# 확률밀도함수 정의
def f(x):
    return b

def g(y):
    return y / a

# 검증 1: f(x)가 [0, a]에서 확률밀도함수
prob_f, _ = integrate.quad(f, 0, a)
print(f'∫f(x)dx = {prob_f}')  # 1.0이어야 함

# 검증 2: g(x)가 [0, a]에서 확률밀도함수
prob_g, _ = integrate.quad(g, 0, a)
print(f'∫g(x)dx = {prob_g}')  # 1.0이어야 함

# 검증 3: g(x) = P(0 ≤ X ≤ x) 확인
for x_test in [0.5, 1.0, 1.5]:
    P_X, _ = integrate.quad(f, 0, x_test)  # P(0 ≤ X ≤ x)
    g_x = g(x_test)  # g(x)
    print(f'P(0≤X≤{x_test}) = {P_X}, g({x_test}) = {g_x}')

# 검증 4: P(0 ≤ Y ≤ c) = 1/2
prob_Y, _ = integrate.quad(g, 0, c)
print(f'P(0≤Y≤{c:.6f}) = {prob_Y}')  # 0.5여야 함

# 최종 답 검증
result = (a + b) * c**2
print(f'(a+b)×c² = ({a}+{b})×{c**2} = {result}')

if abs(prob_f - 1.0) < 1e-10 and abs(prob_g - 1.0) < 1e-10 and abs(prob_Y - 0.5) < 1e-10 and abs(result - 5) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')