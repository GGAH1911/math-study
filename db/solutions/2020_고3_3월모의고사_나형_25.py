# 10<=x<1000, log x^3 - log(1/x^2) = 5 log x = 자연수 n 인 x 개수?  x=10^(n/5)
CANDIDATE = 10
cnt = sum(1 for n in range(1, 100) if 10 <= 10**(n/5) < 1000)
print('VERIFY_PASS' if cnt == CANDIDATE else 'VERIFY_FAIL')
