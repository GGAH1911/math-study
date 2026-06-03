from sympy import *

c_sq = 9
c_val = sqrt(c_sq)
a_sq = c_sq + 18  # 27
b_sq = 18

# P 좌표
x0 = Rational(-27, 9)  # -3
y0 = 6*sqrt(3)/c_val   # 2√3

# 1) P가 원래 타원 위에 있는지
on_ell = simplify(x0**2/a_sq + y0**2/b_sq - 1)

# 2) 접선의 x축 교점 Q, y축 교점 R
Q_x = Rational(a_sq, 1)/x0   # -9
R_y = Rational(b_sq, 1)/y0   # 3√3

F_pt  = Matrix([c_val, 0])
Fp_pt = Matrix([-c_val, 0])
Q_pt  = Matrix([Q_x, 0])
R_pt  = Matrix([0, R_y])

# 3) F'이 QF의 중점인지
mid_QF = (Q_pt + F_pt) / 2
mid_ok = simplify(mid_QF - Fp_pt) == Matrix([0, 0])

# 4) 삼각형 RF'F 정삼각형
d_FF  = simplify(sqrt((F_pt - Fp_pt).dot(F_pt - Fp_pt)))
d_RF  = simplify(sqrt((R_pt - F_pt).dot(R_pt - F_pt)))
d_RFp = simplify(sqrt((R_pt - Fp_pt).dot(R_pt - Fp_pt)))
equi_ok = simplify(d_FF - d_RF) == 0 and simplify(d_FF - d_RFp) == 0

if simplify(on_ell) == 0 and mid_ok and equi_ok:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print('on_ell=', on_ell, 'mid_ok=', mid_ok, 'equi_ok=', equi_ok)
