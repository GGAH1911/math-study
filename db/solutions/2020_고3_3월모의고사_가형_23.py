import sympy as sp
# 중심각 1라디안, 둘레 24인 부채꼴 넓이? 둘레=2r+rθ=3r=24→r=8, 넓이=½r²θ
CANDIDATE = 32
r = sp.symbols('r', positive=True)
rv = sp.solve(2*r + r*1 - 24, r)[0]
print('VERIFY_PASS' if sp.Rational(1, 2)*rv**2*1 == CANDIDATE else 'VERIFY_FAIL')
