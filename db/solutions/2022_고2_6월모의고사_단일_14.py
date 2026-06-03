import sympy as sp

a = sp.log(5, 3)  # 3^a = 5 이므로
b = -a

# 점 A: y = 3^a
y_A = 3**a

# 점 B: y = (1/3)^b - 6
y_B = sp.Rational(1,3)**b - 6

# 중점 x좌표
mid_x = (a + b) / 2

# 중점 y좌표
mid_y = (y_A + y_B) / 2

# 검증
mid_x_val = sp.simplify(mid_x)
mid_y_val = sp.simplify(mid_y)
y_A_val = sp.simplify(y_A)

if sp.simplify(mid_x_val - 0) == 0 and sp.simplify(mid_y_val - 2) == 0 and sp.simplify(y_A_val - 5) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL mid_x={mid_x_val}, mid_y={mid_y_val}, y_A={y_A_val}')
