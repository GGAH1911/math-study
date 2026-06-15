import math

# 2020 9월모평 나형 26: x^2-(2n-1)x+n(n-1)=0 의 두 근 α_n,β_n.
# sum_{n=1}^{81} 1/(√α_n + √β_n) ?  (근은 계수에서 직접 도출)
CANDIDATE = 9
total = 0.0
for n in range(1, 82):
    s = 2 * n - 1            # α+β
    p = n * (n - 1)          # αβ
    disc = s * s - 4 * p     # (α-β)^2 = 1
    r1 = (s + math.sqrt(disc)) / 2
    r2 = (s - math.sqrt(disc)) / 2
    hi, lo = max(r1, r2), min(r1, r2)
    total += 1 / (math.sqrt(hi) + math.sqrt(lo))
print('VERIFY_PASS' if abs(total - CANDIDATE) < 1e-9 else 'VERIFY_FAIL')
