from sympy import binomial, Integer
CANDIDATE = 256
val = sum(binomial(4, k) * Integer(3)**k for k in range(5))
# closed form check via binomial theorem (1+3)^4
closed = Integer(1+3)**4
if val == closed and val == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
