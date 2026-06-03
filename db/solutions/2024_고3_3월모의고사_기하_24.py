import math

# 포물선 y^2 = 20x, PF = 15
# 포물선의 정의: PF = x + p = x + 5
x = 10
p = 5  # 4p = 20

# 준선 정의로 PF 계산
pf_by_definition = x + p

# 직접 거리 계산 (F = (5, 0), P = (10, 10*sqrt(2)))
y = math.sqrt(20 * x)
fx, fy = 5, 0
pf_direct = math.sqrt((x - fx)**2 + (y - fy)**2)

if abs(pf_by_definition - 15) < 1e-9 and abs(pf_direct - 15) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
