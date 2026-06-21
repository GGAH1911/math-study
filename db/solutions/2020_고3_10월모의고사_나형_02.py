from sympy import binomial

n, r = 4, 2
# 중복순열 nПr = n^r
Pi = n**r
# 중복조합 nHr = C(n+r-1, r)
H = binomial(n + r - 1, r)
result = Pi + H
expected = 26
print('Pi =', Pi, 'H =', H, 'sum =', result)
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
