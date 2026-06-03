from sympy import symbols, solve, Eq

x, y = symbols('x y')

# 두 직선의 교점
l1 = Eq(x + 3*y + 2, 0)
l2 = Eq(2*x - 3*y - 14, 0)
pt = solve([l1, l2], [x, y])

# 교점 확인
assert pt[x] == 4 and pt[y] == -2, 'VERIFY_FAIL: 교점 오류'

# 답: x절편 = 3
answer = 3

# 구한 직선: 2x + y - 6 = 0
# 1) 교점을 지나는지
val_at_pt = 2*pt[x] + pt[y] - 6
assert val_at_pt == 0, 'VERIFY_FAIL: 교점 불통과'

# 2) 2x+y+1=0과 평행 (기울기 동일, 절편 상이)
slope_orig = -2  # 2x+y+1=0 → y=-2x-1
slope_new  = -2  # 2x+y-6=0 → y=-2x+6
assert slope_orig == slope_new, 'VERIFY_FAIL: 평행 조건 불만족'
assert 1 != -6, 'VERIFY_FAIL: 동일 직선'

# 3) x절편 확인 (y=0)
x_intercept = solve(Eq(2*x + 0 - 6, 0), x)[0]
assert x_intercept == answer, f'VERIFY_FAIL: x절편={x_intercept}'

print('VERIFY_PASS')
