import sympy as sp
t = sp.Symbol('t', real=True)
a_val = sp.Rational(-5, 2)

# 속력의 제곱 계산
v_sq_at_3pi4 = (a_val + sp.sec(3*sp.pi/4)**2)**2 + (sp.sec(3*sp.pi/4)*sp.tan(3*sp.pi/4))**2
v_sq_at_pi = (a_val + sp.sec(sp.pi)**2)**2 + (sp.sec(sp.pi)*sp.tan(sp.pi))**2

# 간단히 정리
v_sq_at_3pi4_simplified = sp.simplify(v_sq_at_3pi4)
v_sq_at_pi_simplified = sp.simplify(v_sq_at_pi)

# 두 값이 같은지 확인
if sp.simplify(v_sq_at_3pi4_simplified - v_sq_at_pi_simplified) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')