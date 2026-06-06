from sympy import symbols, solve, summation

n = symbols('n', integer=True, positive=True)
x = symbols('x')

# 원래 이차방정식
eq = (n**2 + 6*n + 5)*x**2 - (n+5)*x - 1

# 각 n값에 대해 두 근의 합 계산
result_sum = 0
for k in range(1, 11):
    coeff_x2 = k**2 + 6*k + 5
    coeff_x = -(k + 5)
    a_k = -coeff_x / coeff_x2  # 근과 계수의 관계
    result_sum += 1 / a_k

if result_sum == 65:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')