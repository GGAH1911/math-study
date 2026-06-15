# Σ_{k=1}^5 k^2 ?
CANDIDATE = 55
print('VERIFY_PASS' if sum(k**2 for k in range(1, 6)) == CANDIDATE else 'VERIFY_FAIL')
