import numpy as np

# 원래 문제 조건: P 원점, C=(1,0), A=(0,-3), B=(-2,2)
P = np.array([0.0, 0.0])
A = np.array([0.0, -3.0])
B = np.array([-2.0, 2.0])
C = np.array([1.0, 0.0])

PA = A - P; PC = C - P; PB = B - P

# 조건 (가) 검증
cond_ga_1 = abs(np.dot(PA, PC)) < 1e-9
cond_ga_2 = abs(np.linalg.norm(PA) / np.linalg.norm(PC) - 3) < 1e-9

# 조건 (나) 검증
pb_pc = np.dot(PB, PC)
rhs1 = -np.sqrt(2)/2 * np.linalg.norm(PB) * np.linalg.norm(PC)
rhs2 = -2 * np.linalg.norm(PC)**2
cond_na_1 = abs(pb_pc - rhs1) < 1e-9
cond_na_2 = abs(rhs1 - rhs2) < 1e-9

# D 계산: 직선 AP(y축)와 선분 BC 교점
# BC: (-2,2)+t*(3,-2), x=0 → t=2/3
t = 2/3
D = B + t * (C - B)

# AD = k * PD 검증 (k=11/2)
AD = D - A
PD = D - P
k_computed = AD[1] / PD[1]
k_expected = 11/2
cond_k = abs(k_computed - k_expected) < 1e-9

all_pass = cond_ga_1 and cond_ga_2 and cond_na_1 and cond_na_2 and cond_k
print('VERIFY_PASS' if all_pass else 'VERIFY_FAIL')
