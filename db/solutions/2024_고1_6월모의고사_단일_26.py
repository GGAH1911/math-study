from sympy import symbols, solve, expand

alpha, beta, k = symbols('alpha beta k', real=False)

# 비에타 정리
sum_roots = 5/3
prod_roots = k/3

# alpha, beta를 k에 대한 함수로 표현
# 3x^2 - 5x + k = 0의 근의 공식
x = symbols('x')
roots_eq = 3*x**2 - 5*x + 8  # k=8 대입
roots = solve(roots_eq, x)
alpha_val = roots[0]
beta_val = roots[1]

# 주어진 조건식 검증
k_val = 8
lhs = (3*alpha_val - k_val)*(alpha_val - 1) + (3*beta_val - k_val)*(beta_val - 1)
lhs_expanded = expand(lhs)

# 수치 계산
lhs_result = complex(lhs_expanded)

if abs(lhs_result - (-10)) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')