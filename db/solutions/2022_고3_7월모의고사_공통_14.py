from sympy import *

sqrt10 = sqrt(10)
sqrt30 = sqrt(30)

# ㄱ: 직각삼각형 ACB, angle ACB=90, AB=14, BC=6 => sin(CBA)=AC/AB
AC = sqrt(14**2 - 6**2)  # 4sqrt(10)
check_gak = simplify(AC / 14 - 2*sqrt10/7) == 0

# ㄴ: AD=-3+2√30, CD=7 → Ptolemy: 4√10·DB=6AD+98, AD²+DB²=196
AD_val = -3 + 2*sqrt30
DB_val = (6*AD_val + 98) / (4*sqrt10)
check_neun = simplify(AD_val**2 + DB_val**2 - 196) == 0

# ㄷ: Area=(1/2)(12√10 + 80sinφ - 12√10 cosφ), max osc amplitude = √(80²+(12√10)²)
max_osc = sqrt(80**2 + (12*sqrt10)**2)   # should be 28√10
max_area = Rational(1,2) * (12*sqrt10 + max_osc)
check_deut = simplify(max_area - 20*sqrt10) == 0
# Verify critical point cos φ = -3/7 is in valid arc range
# phi_C = arccos(31/49) ≈ 0.887 rad, critical phi = arccos(-3/7) ≈ 2.014 rad < pi
phi_crit = acos(Rational(-3,7))
phi_C = acos(Rational(31,49))
check_range = bool(phi_crit > phi_C) and bool(phi_crit < pi)

if check_gak and check_neun and check_deut and check_range:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'gak={check_gak}, neun={check_neun}, deut={check_deut}, range={check_range}')
