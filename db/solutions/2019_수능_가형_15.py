from scipy.stats import norm
mu, sigma = 66.4, 15
p_above = 1 - norm.cdf(73, mu, sigma)  # P(X >= 73)
p_below = norm.cdf(73, mu, sigma)      # P(X < 73)
# Using given P(0<=Z<=0.44)=0.17 approximation
p_above_given = 0.5 - 0.17  # = 0.33
p_below_given = 1 - p_above_given  # = 0.67
CANDIDATE = 0.40 * p_above_given + 0.20 * p_below_given
import math
print('VERIFY_PASS' if math.isclose(CANDIDATE, 0.266, abs_tol=1e-9) else f'VERIFY_FAIL: got {CANDIDATE}')