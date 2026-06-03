import math

k = 5

def f(x):
    if x < 0:
        return -4 * x * math.exp(4 * x**2)
    elif x <= k:
        return 0.0
    else:
        return 2 * (x - k) * math.exp((x - k)**2)

# 1) 적분 조건 검증 (해석적): int_k^7 2(x-k)exp((x-k)^2)dx = exp((7-k)^2)-1
integral_analytic = math.exp((7 - k)**2) - 1
expected_integral = math.e**4 - 1
integral_ok = abs(integral_analytic - expected_integral) < 1e-12

# 2) 근 조건 검증: t = 4e^4이면 g(t)=-1, h(t)=k-2*(-1)=7
t_test = 4 * math.e**4
g_test = -1.0  # f(-1) = 4*1*exp(4) = 4e^4
h_test = k - 2 * g_test  # = 7
f_g = -4 * g_test * math.exp(4 * g_test**2)  # = 4e^4
f_h = f(h_test)  # = 2*(7-5)*exp(4) = 4e^4
roots_ok = (abs(f_g - t_test) < 1e-10) and (abs(f_h - t_test) < 1e-10)
constraint_ok = abs(2 * g_test + h_test - k) < 1e-12

# 3) f(9)/f(8) 검증
f9 = f(9)  # 2*4*exp(16) = 8e^16
f8 = f(8)  # 2*3*exp(9)  = 6e^9
ratio = f9 / f8
expected_ratio = (4 / 3) * math.e**7
ratio_ok = abs(ratio - expected_ratio) / expected_ratio < 1e-12

if integral_ok and roots_ok and constraint_ok and ratio_ok:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: integral_ok={integral_ok}, roots_ok={roots_ok}, constraint_ok={constraint_ok}, ratio_ok={ratio_ok}')
