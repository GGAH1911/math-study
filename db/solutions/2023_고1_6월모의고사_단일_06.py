import sympy as sp

x, k = sp.symbols('x k', real=True)

# 원래 문제: 이차함수 y = x^2 + 5x + 9와 직선 y = x + k가 만나지 않음
# 교점 조건: x^2 + 5x + 9 = x + k
# 정리: x^2 + 4x + (9-k) = 0

# k = 4일 때 판별식 확인
k_val = 4
eq = x**2 + 4*x + (9 - k_val)
discriminant = 16 - 4*(9 - k_val)

if discriminant < 0:
    print('VERIFY_PASS')  # k=4일 때 교점 없음
else:
    print('VERIFY_FAIL')

# 경계 확인: k=5일 때는 판별식=0 (접함)
k_boundary = 5
disc_boundary = 16 - 4*(9 - k_boundary)

if disc_boundary >= 0:  # k>=5일 때는 만남
    print('VERIFY_PASS')  # 조건 만족
else:
    print('VERIFY_FAIL')