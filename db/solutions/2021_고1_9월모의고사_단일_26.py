from sympy import symbols, sqrt

m, n = 4, 5
center_x = -1 + m
center_y = -2 + n
radius = 3

# 조건 (가): 제1사분면
if center_x > 0 and center_y > 0:
    cond_a = True
else:
    cond_a = False

# 조건 (나): x축과 y축에 동시에 접함
dist_to_x_axis = abs(center_y)
dist_to_y_axis = abs(center_x)

if dist_to_x_axis == radius and dist_to_y_axis == radius:
    cond_b = True
else:
    cond_b = False

if cond_a and cond_b:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')