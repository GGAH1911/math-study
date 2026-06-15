from sympy import symbols, solve, simplify

a = symbols('a')

# 외분점: 1:2로 외분
# 공식: ((m*x2 - n*x1)/(m-n), (m*y2 - n*y1)/(m-n), (m*z2 - n*z1)/(m-n))
# A(1,0,2), B(2,0,a), m=1, n=2

# z 좌표
z_coord = (1 * a - 2 * 2) / (1 - 2)
z_coord = simplify(z_coord)

# 원점이므로 z_coord = 0
eq = z_coord
sol = solve(eq, a)

if sol and sol[0] == 4:
    # 검증: a=4일 때 외분점이 (0,0,0)인지 확인
    x_point = (1 * 2 - 2 * 1) / (1 - 2)
    y_point = (1 * 0 - 2 * 0) / (1 - 2)
    z_point = (1 * 4 - 2 * 2) / (1 - 2)
    
    if x_point == 0 and y_point == 0 and z_point == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')