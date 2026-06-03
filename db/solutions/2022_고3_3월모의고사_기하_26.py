import sympy as sp

x_val = sp.Rational(5, 4)

# 타원 방정식 확인
ellipse_check = x_val**2 / 25

# PF = 4 (F = (4,0))
PF_sq = (x_val - 4)**2
y_sq = sp.Rational(16, 1) - PF_sq  # from PF=4
ellipse_lhs = x_val**2 / 25 + y_sq / 9

# PF' = 6 (F' = (-4,0))
PF_prime_sq = (x_val + 4)**2 + y_sq

# arithmetic sequence check: PF=4, PF'=6, FF'=8
PF = sp.sqrt((x_val - 4)**2 + y_sq)
PF_prime = sp.sqrt((x_val + 4)**2 + y_sq)
FF = sp.Integer(8)

arith_check = (PF_prime - PF) == (FF - PF_prime)
ellipse_ok = sp.simplify(ellipse_lhs - 1) == 0
first_quadrant = x_val > 0 and y_sq > 0

if ellipse_ok and arith_check and first_quadrant:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print('ellipse_ok:', ellipse_ok, 'arith_check:', arith_check, 'y_sq:', y_sq)
