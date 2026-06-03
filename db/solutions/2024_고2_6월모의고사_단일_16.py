from sympy import sqrt, Rational
BC_CD = 10
cos_BCD = Rational(-1, 5)
sin_BCD = 2*sqrt(6)/5
BD_squared = 33
# 코사인 법칙: BD² = BC² + CD² - 2·BC·CD·cos(∠BCD)
# BC² + CD² = 29 (위에서 유도)
BC_sq_plus_CD_sq = 29
verify_BD_sq = BC_sq_plus_CD_sq - 2*BC_CD*cos_BCD
if verify_BD_sq == BD_squared:
  area_BCD = Rational(1,2) * BC_CD * sin_BCD
  expected_area = 2*sqrt(6)
  if area_BCD == expected_area:
    print('VERIFY_PASS')
  else:
    print('VERIFY_FAIL')
else:
  print('VERIFY_FAIL')