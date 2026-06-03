import sympy as sp
x, y = sp.symbols('x y')
# 원래 두 직선의 교점 찾기
line1 = 3*x + 2*y - 5
line2 = 3*x + y - 1
intersection = sp.solve([line1, line2], [x, y])
pt = (intersection[x], intersection[y])
# 평행한 직선이 이 점을 지나는지 확인
parallel_line = 2*x - y + 6
check = parallel_line.subs({x: pt[0], y: pt[1]})
if check == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')