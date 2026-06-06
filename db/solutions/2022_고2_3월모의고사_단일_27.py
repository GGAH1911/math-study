from sympy import symbols, sqrt, simplify
import math

a, b, r = 3, 4, 5

# 조건 (가): 원 C의 중심 (1,0)이 원 C' 위에 있나?
cond_ga = (1 - (1+a))**2 + (0 - b)**2 == r**2
print(f'조건 (가): {a}^2 + {b}^2 = {a**2 + b**2}, r^2 = {r**2}, 만족: {cond_ga}')

# 조건 (나): 직선이 두 원에 모두 접하는가?
# 점 (1, 0)에서 직선 4x - 3y + 21 = 0까지 거리
dist_C = abs(4*1 - 3*0 + 21) / sqrt(16 + 9)
dist_C = abs(4*1 - 3*0 + 21) / 5
print(f'점 (1,0)에서 직선까지 거리: {dist_C} = {float(dist_C)}, r = {r}')

# 점 (1+a, b)에서 직선까지 거리
dist_C_prime = abs(4*(1+a) - 3*b + 21) / 5
print(f'점 ({1+a},{b})에서 직선까지 거리: {dist_C_prime} = {float(dist_C_prime)}, r = {r}')

if dist_C == r and dist_C_prime == r:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')