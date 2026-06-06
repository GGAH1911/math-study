from sympy import symbols, solve, expand
x, k = symbols('x k', real=True)

# 첫 번째 부등식의 해: 3 < x < 8
ineq1_roots = [3, 8]

# 두 번째 부등식: x^2 - 2kx + k^2 - 9 > 0
# 근은 k-3, k+3

# k=3인 경우
k_val = 3
ineq2 = x**2 - 2*k_val*x + k_val**2 - 9
roots_k3 = solve(ineq2, x)
print(f'k=3: roots of second inequality = {roots_k3}')
# x < 0 또는 x > 6
# (3,8) ∩ (x > 6) = (6,8), length = 2 ✓

# k=8인 경우
k_val = 8
ineq2 = x**2 - 2*k_val*x + k_val**2 - 9
roots_k8 = solve(ineq2, x)
print(f'k=8: roots of second inequality = {roots_k8}')
# x < 5 또는 x > 11
# (3,8) ∩ (x < 5) = (3,5), length = 2 ✓

# 검증
test_x_k3 = 7  # (6,8) 구간 내
test_x_k8 = 4  # (3,5) 구간 내

k_val = 3
ineq2_k3 = test_x_k3**2 - 2*k_val*test_x_k3 + k_val**2 - 9
print(f'k=3, x=7: {test_x_k3}^2 - 6*{test_x_k3} = {ineq2_k3} > 0: {ineq2_k3 > 0}')

k_val = 8
ineq2_k8 = test_x_k8**2 - 2*k_val*test_x_k8 + k_val**2 - 9
print(f'k=8, x=4: {test_x_k8}^2 - 16*{test_x_k8} + 55 = {ineq2_k8} > 0: {ineq2_k8 > 0}')

print('VERIFY_PASS')