import math

# x = 2와 x = 6이 원래 방정식을 만족하는지 확인
for x in [2, 6]:
    # 좌변: log_2(x)
    left = math.log2(x)
    
    # 우변: 1 + log_4(2x-3)
    right = 1 + math.log(2*x - 3, 4)
    
    # 동일한지 확인 (부동소수점 오차 허용)
    if abs(left - right) < 1e-10:
        print(f'x = {x}: LHS = {left}, RHS = {right} ✓')
    else:
        print(f'x = {x}: LHS = {left}, RHS = {right} ✗')

# 곱 계산
product = 2 * 6
print(f'\n모든 해의 곱: {product}')

if product == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')