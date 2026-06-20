import numpy as np
from scipy.optimize import fsolve

# u = tan(u)의 근을 구한다 (홀수 번째만 - 극댓값)
roots = []
for n in range(1, 12, 2):  # n = 1, 3, 5, 7, 9, 11
    # 근은 n*pi와 n*pi + pi/2 사이에 있다
    lower = n * np.pi
    upper = n * np.pi + np.pi/2
    guess = (lower + upper) / 2
    root = fsolve(lambda u: u - np.tan(u), guess)[0]
    roots.append(root)

# a_6은 6번째 극댓값
u_11 = roots[5]  # 6번째 홀수 인덱스 = u_11
a_6 = (u_11 / np.pi) ** 2

# k^2 < a_6 < (k+1)^2를 만족하는 k를 찾는다
k = int(np.sqrt(a_6))
if k**2 < a_6 < (k+1)**2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')