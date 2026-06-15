# 2020 9월모평 가형 25: 모비율 신뢰구간. p_hat=0.9, 신뢰도 95%(z=1.96),
# 오차한계 c = z*sqrt(p_hat(1-p_hat)/n) = 0.0294. n?
CANDIDATE = 400
p_hat = 0.9
z = 1.96
c = 0.0294
n_exact = p_hat * (1 - p_hat) * (z / c) ** 2     # n = p(1-p)(z/c)^2
print('VERIFY_PASS' if abs(n_exact - CANDIDATE) < 0.5 else 'VERIFY_FAIL')
