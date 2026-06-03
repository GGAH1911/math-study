import sympy as sp

# 벡터 a, b를 기호로 정의
a1, a2, b1, b2 = sp.symbols('a1 a2 b1 b2', real=True)

# 첫 번째 벡터
v1 = (-1, 2)  # -a + 2b의 계수

# k=4일 때 두 번째 벡터
k = 4
v2 = (-2, k)  # -2a + kb의 계수

# 평행 조건: v1 = λ * v2
# (-1, 2) = λ * (-2, 4)
lambda_val = sp.Rational(-1, -2)  # = 1/2

# 확인: v2 = (1/lambda_val) * v1
if v1[0] * v2[1] == v1[1] * v2[0]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')