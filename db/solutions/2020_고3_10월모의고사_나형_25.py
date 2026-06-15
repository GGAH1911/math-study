from sympy import Rational
# f(x)=(1+x⁴+x⁸+x¹²)(1+x+x²+x³). f(2)/((f(1)-1)(f(1)+1))?
CANDIDATE = 257
f = lambda x: (1+x**4+x**8+x**12)*(1+x+x**2+x**3)
val = Rational(f(2), (f(1)-1)*(f(1)+1))
print('VERIFY_PASS' if val == CANDIDATE else 'VERIFY_FAIL')
