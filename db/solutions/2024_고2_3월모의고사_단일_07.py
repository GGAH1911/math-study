import numpy as np

# 정수해 집합
integers = [-3, -2, -1, 0]
count = 0

for x in integers:
    # 조건 1: 2x + 1 < 3
    cond1 = 2*x + 1 < 3
    # 조건 2: x^2 - 2x - 15 <= 0
    cond2 = x**2 - 2*x - 15 <= 0
    
    if cond1 and cond2:
        count += 1

# x=1은 만족하지 않는지 확인
if 2*1 + 1 >= 3:  # 2 + 1 = 3이므로 < 3 불만족
    x_boundary_fail = True
else:
    x_boundary_fail = False

if count == 4 and x_boundary_fail:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')