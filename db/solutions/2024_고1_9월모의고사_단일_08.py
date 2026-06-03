from sympy import symbols, factor, solve
x, a, b = symbols('x a b', real=True)
# 원래 식: x^2 + ax - 12 <= 0의 해가 -4 <= x <= b
# 따라서 x^2 + ax - 12 = 0의 근이 -4와 b
# 비에타 정리: (-4) * b = -12, -4 + b = -a
b_val = 3  # -4b = -12에서
a_val = 1  # -4 + 3 = -a에서

# 검증: x^2 + ax - 12 = 0에 x = -4, x = b를 대입
quadratic = x**2 + a_val*x - 12
root1_check = quadratic.subs(x, -4)
root2_check = quadratic.subs(x, b_val)

if root1_check == 0 and root2_check == 0:
    answer = a_val - b_val
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')