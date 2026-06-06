import math
mu=3.4
# sigma from P(X<=3.9)=P(Z<=1): (3.9-mu)/sigma=1
sigma=(3.9-mu)/1.0
assert abs(sigma-0.5)<1e-9
n=25
se=sigma/math.sqrt(n)
z=(3.55-mu)/se
assert abs(z-1.5)<1e-9
P=0.5-0.4332
print('VERIFY_PASS' if abs(P-0.0668)<1e-9 else 'VERIFY_FAIL')