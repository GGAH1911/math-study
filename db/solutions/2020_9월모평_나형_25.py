import sympy as sp

# 2020 9월모평 나형 25: 모평균 신뢰구간(95%, z=1.96), n=64. 폭 b-a = 2*z*σ/√n = 4.9. σ?
CANDIDATE = 10
s = sp.symbols('s', positive=True)
z = sp.Rational(196, 100)        # 1.96
width = sp.Rational(49, 10)      # 4.9
sol = sp.solve(2 * z * s / sp.sqrt(64) - width, s)[0]
print('VERIFY_PASS' if sol == CANDIDATE else 'VERIFY_FAIL')
