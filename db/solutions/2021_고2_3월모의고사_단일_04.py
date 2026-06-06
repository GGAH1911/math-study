from math import factorial
def P(n, r):
    return factorial(n) // factorial(n - r)
def C(n, r):
    return factorial(n) // (factorial(r) * factorial(n - r))

P_10_3 = P(10, 3)
C_10_3 = C(10, 3)
answer = 6

if P_10_3 == answer * C_10_3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')