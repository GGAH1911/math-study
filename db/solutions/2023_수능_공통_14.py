# 검증: ㄱ h(1) = 3
# g 정의: x < -1 또는 x > 1일 때 g(x) = x, -1≤x≤1일 때 g(x) = f(x)
# h(x) = lim_{t→0+} g(x+t) × lim_{t→2-} g(x+t)
# x=1에서: 1+t > 1이므로
lim_t0_plus = 1  # g(1+t) = 1+t → 1
lim_t2_minus = 3  # g(1+t) = 1+t → 3
h_1 = lim_t0_plus * lim_t2_minus
print('VERIFY_PASS' if h_1 == 3 else 'VERIFY_FAIL')