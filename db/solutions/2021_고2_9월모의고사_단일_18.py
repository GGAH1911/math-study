import sympy as sp
a=sp.Integer(1); b=sp.Integer(-1)
for n in range(1,2021):
    a,b=a+b, sp.nsimplify(2*sp.cos(a/3*sp.pi))
print('VERIFY_PASS' if a-b==6 else 'VERIFY_FAIL')