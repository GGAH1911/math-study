from sympy import Rational

def S(n):
    return sum(Rational((-1)**(k-1), k) for k in range(1, 2*n+1))

def T(n):
    return sum(Rational(1, n+k) for k in range(1, n+1))

# (star) identity holds for tested n
assert all(S(n) == T(n) for n in range(1, 13)), 'star identity fails'

# (ga): a = S_1
a = S(1)
assert a == Rational(1, 2)

# f(m) = (na): S_{m+1} = S_m + 1/(2m+1) + f(m)
def f(m):
    return S(m+1) - S(m) - Rational(1, 2*m+1)
for m in range(1, 13):
    assert f(m) == -Rational(1, 2*m+2), 'f mismatch'

# g(m) = (da): T_{m+1} = T_m + g(m) + 1/(2m+1) + 1/(2m+2)
def g(m):
    return T(m+1) - T(m) - Rational(1, 2*m+1) - Rational(1, 2*m+2)
for m in range(1, 13):
    assert g(m) == -Rational(1, m+1), 'g mismatch'

result = a + g(5)/f(14)
CANDIDATE = Rational(11, 2)
print('VERIFY_PASS' if result == CANDIDATE else 'VERIFY_FAIL')
