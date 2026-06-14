from sympy import Rational, summation, symbols
n = symbols('n', integer=True)
a = lambda k: 2*k+1
expr = Rational(1,1)/(a(n)*a(n+2-1))
# a_n=2n+1, a_{n+1}=2(n+1)+1=2n+3
term = Rational(1,1)/((2*n+1)*(2*n+3))
S = summation(term, (n, 1, 12))
CANDIDATE = Rational(4,27)
print('VERIFY_PASS' if S == CANDIDATE else 'VERIFY_FAIL')
