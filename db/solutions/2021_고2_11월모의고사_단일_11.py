import sympy as sp
x=sp.symbols('x')
a,b=2,3
f=4*sp.cos(sp.pi/a*x)+b
period=2*sp.pi/(sp.pi/a)
min_val=-4+b
ok = (period==4) and (min_val==-1) and (a+b==5)
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')