import sympy as sp

x, y = sp.symbols('x y', real=True)

# 원래 연립방정식
eq1 = x - y + 5  # x - y = -5
eq2 = 4*x**2 + y**2 - 20  # 4x^2 + y^2 = 20

# 해를 구함
solutions = sp.solve([eq1, eq2], [x, y])
print(f'Solutions: {solutions}')

# 네 답 검증
alpha, beta = -1, 4

# 첫 번째 식 검증
check1 = alpha - beta
print(f'x - y = {check1}, should be -5: {check1 == -5}')

# 두 번째 식 검증
check2 = 4*alpha**2 + beta**2
print(f'4x^2 + y^2 = {check2}, should be 20: {check2 == 20}')

# 두 조건이 모두 만족되면
if check1 == -5 and check2 == 20:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')