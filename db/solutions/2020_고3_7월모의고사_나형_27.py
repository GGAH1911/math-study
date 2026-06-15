import math
# 0<=x<2^{n+1}, cos(πx/2^n)<=-1/2 인 자연수 x 개수 a_n. Σ_{1}^{7} a_n?
CANDIDATE = 169
total = 0
for n in range(1, 8):
    total += sum(1 for x in range(1, 2**(n+1))
                 if math.cos(math.pi*x/2**n) <= -0.5 + 1e-9)
print('VERIFY_PASS' if total == CANDIDATE else 'VERIFY_FAIL')
