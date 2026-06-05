import sympy as sp
a, b = 8, 8
x, y = sp.symbols('x y', real=True)
# 포물선 방정식 y^2 = ax + b
# 1) 꼭짓점 확인: y=0일 때 x = -b/a 가 꼭짓점 x좌표
vertex_x = sp.Rational(-b, a)
vertex_ok = (vertex_x == -1)
# 2) 준선 확인: y^2 = 4p(x-h), 4p = a => p = a/4, 준선 x = h - p
h = vertex_x
p = sp.Rational(a, 4)
directrix_x = h - p
directrix_ok = (directrix_x == -3)
# 3) a+b 합 확인
sum_ok = (a + b == 16)
if vertex_ok and directrix_ok and sum_ok:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
