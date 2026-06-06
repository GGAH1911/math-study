import cmath
import math

# 원래 방정식의 한 허근
omega = 1 + 1j

# omega*(omega-1) 계산
product = omega * (omega - 1)

# 절댓값
abs_product = abs(product)

# n=16일 때 확인
n = 16
result = abs_product ** n

print(f'omega = {omega}')
print(f'omega*(omega-1) = {product}')
print(f'|omega*(omega-1)| = {abs_product}')
print(f'|omega*(omega-1)|^{n} = {result}')

if abs(result - 256) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')