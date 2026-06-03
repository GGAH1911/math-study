import sympy as sp
k = 192
S = [0] * 7
S[1] = k / 2
for n in range(2, 7):
    S[n] = (S[n-1] + k) / 2
print('VERIFY_PASS' if abs(S[6] - 189) < 1e-9 else 'VERIFY_FAIL')