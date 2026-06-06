import sympy as sp
from sympy import sqrt, cos, acos, symbols, Abs, simplify

# 좌표 정의
x_P, y_P = 2, 2*sqrt(15)
x_Q, y_Q = -sp.Rational(7,4), 7*sqrt(15)/4

# 조건 검증
AP = sqrt((x_P - 2)**2 + y_P**2)
AQ = sqrt((x_Q - 2)**2 + y_Q**2)
OP = sqrt(x_P**2 + y_P**2)
OQ = sqrt(x_Q**2 + y_Q**2)

assert simplify(AP - 2*sqrt(15)) == 0, f'AP check failed: {AP}'
assert simplify(AQ - 2*sqrt(15)) == 0, f'AQ check failed: {AQ}'
assert OP > OQ, f'OP > OQ check failed: {OP} > {OQ}'

# 코사인 조건 검증
vec_PO = (-x_P, -y_P)
vec_PA = (2 - x_P, -y_P)
dot_P = vec_PO[0]*vec_PA[0] + vec_PO[1]*vec_PA[1]
cos_OPA = dot_P / (OP * AP)

vec_QO = (-x_Q, -y_Q)
vec_QA = (2 - x_Q, -y_Q)
dot_Q = vec_QO[0]*vec_QA[0] + vec_QO[1]*vec_QA[1]
cos_OQA = dot_Q / (OQ * AQ)

assert simplify(cos_OPA - sqrt(15)/4) == 0, f'cos(∠OPA) check: {cos_OPA}'
assert simplify(cos_OQA - sqrt(15)/4) == 0, f'cos(∠OQA) check: {cos_OQA}'

# 넓이 계산 (신발끈)
area = abs((0*0 - 2*0) + (2*2*sqrt(15) - 2*0) + (2*7*sqrt(15)/4 - (-sp.Rational(7,4))*2*sqrt(15)) + ((-sp.Rational(7,4))*0 - 0*7*sqrt(15)/4)) / 2
area = simplify(area)

expected_area = 11*sqrt(15)/2
assert simplify(area - expected_area) == 0, f'Area check: {area} vs {expected_area}'

# p × q 계산
print('VERIFY_PASS')