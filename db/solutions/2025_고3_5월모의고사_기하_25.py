from sympy import symbols, solve, simplify
p = symbols('p', positive=True, real=True)
# 포물선 위의 점 (1/p, 2)에서의 접선
# 접선: y = px + 1
# 준선 x = -p와의 교점 y좌표
y_intercept = -p**2 + 1
# 주어진 조건: y좌표 = -5/4
eq = y_intercept + 5/4
sol = solve(eq, p)
for s in sol:
    if s > 0:
        p_val = s
print(f'p = {p_val}')
# 검증: p = 3/2일 때
p_check = 3/2
y_check = -p_check**2 + 1
print(f'y = {y_check}')
if abs(y_check - (-5/4)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')