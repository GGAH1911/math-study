from sympy import symbols, solve, sqrt
p = symbols('p', positive=True)
# 포물선 위의 점 (4p, 4p)
x, y = 4*p, 4*p
# 포물선 방정식 검증: y^2 = 4px
check_parabola = y**2 - 4*p*x
# p=4일 때 거리 검증: P와 준선 x=-p 사이의 거리
distance = (4*p) - (-p)
# p=4를 대입하여 조건 확인
p_val = 4
dist_val = 5*p_val
if check_parabola.subs(p, p_val) == 0 and dist_val == 20:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')