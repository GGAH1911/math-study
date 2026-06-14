CANDIDATE = 9

from sympy import symbols, solve, simplify

# t=2일 때 각 점의 좌표
t_val = 2

# 곡선 y=3^(2-x)+8에서 x=t일 때
A_y = 3**(2-t_val) + 8
assert A_y == 9, f'A_y should be 9, got {A_y}'

# 곡선 y=3^(x-1)에서 x=t+1일 때
D_y = 3**(t_val+1-1)
assert D_y == 9, f'D_y should be 9, got {D_y}'

# 직사각형의 가로와 세로
width = 1  # (t+1) - t
height = 9  # A_y - 0

area = width * height

if area == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')