# Σa=3, Σ(a+b)=9 → Σb=6. Σ_{1}^{10}(b_k+k) = Σb + Σk?
CANDIDATE = 61
Sb = 9 - 3
print('VERIFY_PASS' if Sb + sum(range(1, 11)) == CANDIDATE else 'VERIFY_FAIL')
