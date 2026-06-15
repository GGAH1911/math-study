import sympy as sp

# 표준정규분포표 (문제 제공)
table = {1.0:0.3413, 1.5:0.4332, 2.0:0.4772, 2.5:0.4938}

# f(t)=P(t<=X<=t+2)가 t=4에서 최대 -> 구간 중점 t+1 = m -> m = 4+1 = 5
m = 4 + 1

# f(m)=P(0<=Z<=2/sigma)=0.3413 -> 2/sigma = 1.0 -> sigma = 2
sigma = sp.Rational(2,1) / 1.0  # 2/sigma=1.0
sigma = sp.nsimplify(2/1.0)

# f(7)=P(7<=X<=9), 표준화 z1=(7-m)/sigma, z2=(9-m)/sigma
z1 = (7 - m)/sigma
z2 = (9 - m)/sigma

# 정규분포 누적: P(z1<=Z<=z2) = P(0<=Z<=z2)-P(0<=Z<=z1)
f7 = table[float(z2)] - table[float(z1)]

expected = 0.1359
if abs(f7 - expected) < 1e-9 and float(m)==5 and float(sigma)==2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')