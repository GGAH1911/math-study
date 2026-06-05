import sympy as sp
theta = sp.Symbol('theta')

# 조건: sin(π + θ) = -1/3
condition = sp.sin(sp.pi + theta) + sp.Rational(1,3)
simplified_condition = sp.simplify(condition)
print(f'Condition check: {simplified_condition} = 0')

# sin(θ) 구하기
sin_theta = sp.Rational(1, 3)
print(f'sin(θ) = {sin_theta}')

# 주어진 식 계산
# sin²θ + cos²θ = 1에서 cos²θ = 1 - sin²θ
cos_squared = 1 - sin_theta**2
print(f'cos²(θ) = {cos_squared}')

# 원래 식: 2*sin(θ) / sin²(θ) = 2 / sin(θ)
result = 2 / sin_theta
print(f'Result: 2 / sin(θ) = 2 / (1/3) = {result}')

if result == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')