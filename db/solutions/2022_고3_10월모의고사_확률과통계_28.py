import math
from statistics import NormalDist
muX, sigma = 20, 2
muY = muX - 6
X = NormalDist(muX, sigma)
Y = NormalDist(muY, sigma)
# (가)
c1 = math.isclose(X.cdf(11), 1 - Y.cdf(23), abs_tol=1e-12)
# g(x)=f(x+6) check
import random
random.seed(0)
shape_ok = all(math.isclose(Y.pdf(x), X.pdf(x+6), abs_tol=1e-12) for x in [random.uniform(-10,30) for _ in range(50)])
# (나) with k=17
k = 17
c2 = math.isclose(X.cdf(k) + Y.cdf(k), 1, abs_tol=1e-12)
# target probability
val = X.cdf(k) + (1 - Y.cdf(k))
c3 = math.isclose(val, 0.1336, abs_tol=5e-5)
ans = muX + sigma
if c1 and shape_ok and c2 and c3 and ans == 22:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
