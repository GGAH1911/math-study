import numpy as np

# 원래 조건: AP=3, BP=3√2, AP/CA = BP/BA = BA/BC
# 좌표
d = 3*np.sqrt(3)
q = np.sqrt(3)
h = np.sqrt(6)
p = 3*np.sqrt(6)/2

A = np.array([p, 0, 0])
B = np.array([p, d, 0])
P = np.array([p, q, h])

CA = d / np.sqrt(2)
C = np.array([p - CA, 0, 0])  # C는 A 기준 l 위

# 검증: AP, BP
AP = np.linalg.norm(P - A)
BP_ = np.linalg.norm(P - B)
assert abs(AP - 3) < 1e-9, f'AP={AP}'
assert abs(BP_ - 3*np.sqrt(2)) < 1e-9, f'BP={BP_}'

# PA ⊥ l, PB ⊥ m
l_dir = np.array([1,0,0])
assert abs(np.dot(P-A, l_dir)) < 1e-9
assert abs(np.dot(P-B, l_dir)) < 1e-9

# 비례 조건
BA = np.linalg.norm(B - A)
BC = np.linalg.norm(C - B)
CA_len = np.linalg.norm(A - C)
r1 = AP / CA_len
r2 = BP_ / BA
r3 = BA / BC
assert abs(r1-r2) < 1e-9 and abs(r2-r3) < 1e-9, f'ratios {r1},{r2},{r3}'

# H: P에서 BC에 내린 수선의 발
BC_vec = C - B
t = np.dot(P - B, BC_vec) / np.dot(BC_vec, BC_vec)
H = B + t * BC_vec
assert abs(np.dot(P - H, BC_vec)) < 1e-9, 'PH not perp BC'

PH = np.linalg.norm(P - H)
expected = np.sqrt(10)
if abs(PH - expected) < 1e-8:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: PH={PH}, expected={expected}')
