from sympy import *

a = log(Rational(3,7), 2)
b = a + 3
c = Rational(3,7) - a  # c = 2^a - a

p = a + 1
q = b + 1

# A on y=2^x and y=x+c
cond1 = simplify(2**a - (a + c))
# B on y=2^x and y=x+c
cond2 = simplify(2**b - (b + c))
# C on y=2^(x-1)+1 and y=x+c
cond3 = simplify(2**(p-1) + 1 - (p + c))
# D on y=2^(x-1)+1 and y=x+c
cond4 = simplify(2**(q-1) + 1 - (q + c))
# B divides AD in ratio 3:1
AB = b - a
BD = q - b
cond5 = simplify(AB / BD - 3)
# B x-coordinate equals log2(24/7)
cond6 = simplify(2**b - Rational(24,7))

if all(c == 0 for c in [cond1, cond2, cond3, cond4, cond5, cond6]):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', cond1, cond2, cond3, cond4, cond5, cond6)
