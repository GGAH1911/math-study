from sympy import isprime, Rational

def next_term(a, n):
    if isprime(a):
        return Rational(a + 3, 2)
    else:
        return a + n

a = {1: Rational(7)}
for n in range(1, 8):
    a[n + 1] = next_term(a[n], n)

a8 = a[8]
CANDIDATE = 17
print('a8 =', a8)
if a8 == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
