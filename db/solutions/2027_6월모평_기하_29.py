import numpy as np
from scipy.optimize import fsolve

# a^2 = 9/5
a_squared = 9/5
a = np.sqrt(a_squared)

# 쌍곡선: x^2/a^2 - y^2/(9-a^2) = 1
# 포물선: y^2 = 4(3+a)(x+a)

# 제1사분면 교점
x1 = 3*a*(a+1)/(3-a)
y1_sq = 4*(3+a)*(x1+a)
y1 = np.sqrt(y1_sq)

# 검증: 쌍곡선 방정식
hyperbola_check1 = x1**2/a_squared - y1**2/(9-a_squared)

# 검증: 포물선 방정식
parabola_check1 = y1**2 - 4*(3+a)*(x1+a)

# 제2사분면 교점
x2 = -3 - 2*a
y2_sq = (9-a_squared) * (((3+2*a)**2 - a_squared)/a_squared)
y2 = np.sqrt(y2_sq)

# 검증: 쌍곡선 방정식
hyperbola_check2 = x2**2/a_squared - y2**2/(9-a_squared)

# 조건 확인
condition_check = abs(y1 - y2)

if condition_check < 1e-10 and abs(hyperbola_check1 - 1) < 1e-10 and abs(hyperbola_check2 - 1) < 1e-10 and abs(parabola_check1) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')