import sympy as sp
# y=k sin(x+π/2)+10 가 (π/3,14) 통과. k?  sin(x+π/2)=cos x
CANDIDATE = 8
k = sp.symbols('k')
print('VERIFY_PASS' if sp.solve(sp.Eq(k*sp.cos(sp.pi/3)+10, 14),k)[0]==CANDIDATE else 'VERIFY_FAIL')
