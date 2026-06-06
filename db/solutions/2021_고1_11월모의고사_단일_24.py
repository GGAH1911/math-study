# 무게중심이 y=x 위에 있는지 확인
x_A, y_A = 2, 6
x_B, y_B = 4, 1
x_C, y_C = 8, 7  # a = 7

# 무게중심
G_x = (x_A + x_B + x_C) / 3
G_y = (y_A + y_B + y_C) / 3

print(f'무게중심: ({G_x}, {G_y})')
print(f'G_x = {G_x}, G_y = {G_y}')

# y = x 위에 있는지 확인
if abs(G_y - G_x) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')