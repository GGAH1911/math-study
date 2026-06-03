from sympy import *
x, y, b_val = symbols('x y b_val', real=True, positive=True)

# 점 (3, sqrt(5))가 타원 위에 있으므로 b^2 구하기
pt_x, pt_y = 3, sqrt(5)
eq1 = Eq(pt_x**2 / 18 + pt_y**2 / b_val**2, 1)
b_squared = solve(eq1, b_val**2)[0]
print(f'b^2 = {b_squared}')

# 타원: x^2/18 + y^2/10 = 1
# 점 (3, sqrt(5))에서의 접선: (3x)/18 + (sqrt(5)*y)/10 = 1
# y절편(x=0): (sqrt(5)*y)/10 = 1 => y = 10/sqrt(5) = 2*sqrt(5)

y_intercept = 10 / sqrt(5)
y_intercept_simplified = simplify(y_intercept)
print(f'y절편 = {y_intercept_simplified}')

# 검증: 접선이 점 (3, sqrt(5))를 지나는가?
tangent_eq = (3*x)/18 + (sqrt(5)*y)/10 - 1
check = tangent_eq.subs([(x, 3), (y, sqrt(5))])
print(f'접선이 점(3,√5)을 지나는가: {check} (0이면 통과)')

# 최종 답 검증
answer = 2*sqrt(5)
if answer == y_intercept_simplified:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')