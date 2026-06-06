import sympy as sp

# 정의: P(A)를 변수로
PA = sp.Rational(1, 3)
PB = sp.Rational(1, 3)
P_A_and_B = sp.Rational(1, 9)

# 검증 1: 독립성 확인
independence_check = (PA * PB == P_A_and_B)

# 검증 2: P(A|B) = P(B) 확인
if PB != 0:
    P_A_given_B = P_A_and_B / PB
    condition_check = (P_A_given_B == PB)
else:
    condition_check = False

if independence_check and condition_check:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')