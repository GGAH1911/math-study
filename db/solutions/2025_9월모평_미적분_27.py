from sympy import *

# 검증: 미분한 방정식 f'(x) + f'(sin(x)/2)*(cos(x)/2) = cos(x) 가
# x=0, x=pi 에서 f'(0)=2/3, f'(pi)=-2/3 을 만족하는지 확인

fp0 = Rational(2, 3)
fp_pi = Rational(-2, 3)

# x=0 검증: f'(0) + f'(sin(0)/2)*(cos(0)/2) = cos(0)
# = f'(0) + f'(0)*(1/2) = 1
lhs_x0 = fp0 + fp0 * Rational(1, 2) * Integer(1)  # cos(0)=1
rhs_x0 = Integer(1)
check1 = (lhs_x0 == rhs_x0)

# x=pi 검증: f'(pi) + f'(sin(pi)/2)*(cos(pi)/2) = cos(pi)
# sin(pi)=0 -> f'(0) 가 들어옴, cos(pi)=-1
lhs_xpi = fp_pi + fp0 * Rational(1, 2) * Integer(-1)  # cos(pi)=-1
rhs_xpi = Integer(-1)
check2 = (lhs_xpi == rhs_xpi)

# 원래 함수방정식 x=0: f(0)+f(0)=0 => f(0)=0 일관성 확인
# (미분 단계의 일관성만 심볼릭으로 검증)
if check1 and check2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'x=0 check: {lhs_x0} == {rhs_x0} -> {check1}')
    print(f'x=pi check: {lhs_xpi} == {rhs_xpi} -> {check2}')
