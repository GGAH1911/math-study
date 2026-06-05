import sympy as sp

# 그래프 분석
# x < 1에서 직선이 (1, 3)을 지남
lim_1_minus = 3

# x > 2에서 수평선 y = 1
lim_2_plus = 1

# 극한값의 합
result = lim_1_minus + lim_2_plus

if result == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')