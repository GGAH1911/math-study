from sympy import Rational, binomial
p = Rational(1,2)
prob = sum(binomial(6,k)*p**k*(1-p)**(6-k) for k in range(2,7))
expected = Rational(57,64)
print('VERIFY_PASS' if prob == expected else 'VERIFY_FAIL')