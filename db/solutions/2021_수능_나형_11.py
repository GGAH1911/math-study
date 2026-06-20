from sympy import sqrt, Rational
mu = 20
sigma = 5
n = 16
E_Xbar = mu
sigma_Xbar = Rational(sigma, 1) / sqrt(n)
result = E_Xbar + sigma_Xbar
expected = Rational(85, 4)
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', result)