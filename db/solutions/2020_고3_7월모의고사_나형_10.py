from sympy import *
a = symbols('a', positive=True)
# A = (1,0), B = (4,2), C = (4, log_a(4))
# log_a(4) = log(4)/log(a)
log_a_4 = log(4)/log(a)
# BC 길이 (수직 선분)
BC = 2 - log_a_4  # 0<a<1 → log_a(4)<0 → BC>0
# 높이: A에서 x=4까지 수평거리 = 4-1 = 3
height = 3
area_expr = Rational(1,2)*BC*height
# 넓이 = 9/2
eq = Eq(area_expr, Rational(9,2))
sol = solve(eq, a)
print('solutions:', sol)
a_val = [s for s in sol if 0 < s < 1]
if a_val:
    a_num = a_val[0]
    area_check = Rational(1,2)*(2 - log(4)/log(a_num))*3
    if simplify(area_check - Rational(9,2)) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')
