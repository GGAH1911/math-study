import sympy as sp
theta = sp.Symbol('theta', real=True)
# 조건: tan(theta) = sqrt(5)/2, pi < theta < 3pi/2
tan_val = sp.Rational(5,4)  # tan^2 = 5/4
sec2 = 1 + tan_val  # sec^2 = 1 + tan^2 = 9/4
cos2 = 1 / sec2   # cos^2 = 4/9
# 제3사분면: cos < 0
cos_val = -sp.sqrt(cos2)  # -2/3
# 검증1: cos^2 + sin^2 = 1 via tan
sin_val = cos_val * (sp.sqrt(5)/2)  # sin = tan * cos, 3사분면 sin<0 확인
# tan = sin/cos = (cos*sqrt(5)/2)/cos = sqrt(5)/2 OK
tan_check = sin_val / cos_val
# 검증2
ok1 = sp.simplify(cos_val + sp.Rational(2,3)) == 0
ok2 = sp.simplify(tan_check - sp.sqrt(5)/2) == 0
ok3 = sin_val < 0  # 제3사분면
if ok1 and ok2 and ok3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', ok1, ok2, ok3)
