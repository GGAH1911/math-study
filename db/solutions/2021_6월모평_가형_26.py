import sympy as sp

a1 = -7
d = 2
k = 4

# S_k = -16 검증
S_k = k * a1 + k * (k - 1)
assert S_k == -16, f'S_k={S_k}, expected -16'

# S_{k+2} = -12 검증
S_k2 = (k+2) * a1 + (k+2) * (k+1)
assert S_k2 == -12, f'S_{{k+2}}={S_k2}, expected -12'

# a_{2k} = a_8 계산
a_2k = a1 + (2*k - 1) * d
assert a_2k == 7, f'a_{{2k}}={a_2k}, expected 7'

print('VERIFY_PASS')