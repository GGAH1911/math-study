import sympy as sp
# y=a sin(bx)+c (a,b>0). max=3,min=-1, 극대 x=π/4,5π/4(주기π). a+b+c? (②=5)
CANDIDATE = 5
mx, mn = 3, -1
a = sp.Rational(mx-mn, 2)               # 2
c = sp.Rational(mx+mn, 2)               # 1
b = 2*sp.pi/(sp.Rational(5,4)*sp.pi - sp.Rational(1,4)*sp.pi)   # 2π/π=2
print('VERIFY_PASS' if a+b+c == CANDIDATE else 'VERIFY_FAIL')
