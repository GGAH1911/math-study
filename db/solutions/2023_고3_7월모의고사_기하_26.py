from sympy import *

t1, p = symbols('t1 p', positive=True)

# 포물선 매개변수: (p*t^2, 2p*t), 초점현: t1*t2=-1
t2 = -1/t1
x1, y1 = p*t1**2, 2*p*t1
x2, y2 = p*t2**2, 2*p*t2

# AC = x1+p, BD = x2+p
AC = x1 + p
BD = x2 + p

# 조건1: AC:BD = 2:1 -> 풀기
t1_val = solve(Eq(AC, 2*BD), t1)[0]
assert simplify(t1_val - sqrt(2)) == 0, 'VERIFY_FAIL: t1'

# 좌표 대입
x1v = x1.subs(t1, t1_val)
y1v = y1.subs(t1, t1_val)
x2v = x2.subs(t1, t1_val)
y2v = y2.subs(t1, t1_val)

# 사각형 ACDB 꼭짓점
xA,yA = x1v, y1v
xC,yC = -p, y1v
xD,yD = -p, y2v
xB,yB = x2v, y2v

# 신발끈 공식
area = Rational(1,2)*Abs(
    (xA*yC - xC*yA) +
    (xC*yD - xD*yC) +
    (xD*yB - xB*yD) +
    (xB*yA - xA*yB)
)
area_s = simplify(area)

# 조건2: 넓이 = 12*sqrt(2)
p_sol = solve(Eq(area_s, 12*sqrt(2)), p)
p_val = p_sol[0]

# AB 계산
AC_v = (x1v + p).subs(p, p_val)
BD_v = (x2v + p).subs(p, p_val)
AB = simplify(AC_v + BD_v)

# 검증
if simplify(AB - 6) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', 'AB=', AB)
