from fractions import Fraction
import math

# 원래 조건: AB=AC=25, BC=40 이등변삼각형, D=C에서 직선AB 수선의 발
# 좌표
Ax, Ay = Fraction(0), Fraction(15)
Bx, By = Fraction(-20), Fraction(0)
Cx, Cy = Fraction(20), Fraction(0)

# AB=25 검증
AB = math.sqrt(float((Ax-Bx)**2+(Ay-By)**2))
AC = math.sqrt(float((Ax-Cx)**2+(Ay-Cy)**2))
BC = math.sqrt(float((Bx-Cx)**2+(By-Cy)**2))
assert abs(AB-25)<1e-9 and abs(AC-25)<1e-9 and abs(BC-40)<1e-9, 'side check fail'

# D: 수선의 발 (직선 3x-4y+60=0)
val = 3*Cx + (-4)*Cy + 60
denom = 3**2 + (-4)**2
Dx = Cx - Fraction(3*val, denom)
Dy = Cy - Fraction(-4*val, denom)

# D가 직선 AB 위에 있고 수직인지 확인
assert 3*Dx - 4*Dy + 60 == 0, 'D not on line AB'
CD = (Dx-Cx, Dy-Cy); AB_dir = (Bx-Ax, By-Ay)
assert CD[0]*AB_dir[0]+CD[1]*AB_dir[1] == 0, 'CD not perpendicular to AB'

# 내심 I (삼각형 ABC, a=40,b=25,c=25)
Ix = (40*Ax + 25*Bx + 25*Cx) / 90
Iy = (40*Ay + 25*By + 25*Cy) / 90

# 삼각형 DBC 변 길이
DC2 = (Dx-Cx)**2+(Dy-Cy)**2
DB2 = (Dx-Bx)**2+(Dy-By)**2
BC2 = (Bx-Cx)**2+(By-Cy)**2
DC_len = math.sqrt(float(DC2))
DB_len = math.sqrt(float(DB2))
BC_len = 40.0

# 내심 J (삼각형 DBC, a'=BC=40, b'=DC=24, c'=DB=32)
total = Fraction(40) + Fraction(round(DC_len)) + Fraction(round(DB_len))
Jx = (40*Dx + 24*Bx + 32*Cx) / 96
Jy = (40*Dy + 24*By + 32*Cy) / 96

# IJ 계산
IJ2 = (Ix-Jx)**2 + (Iy-Jy)**2
IJ = math.sqrt(float(IJ2))
expected = 4*math.sqrt(10)/3

if abs(IJ - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: IJ={IJ}, expected={expected}')
