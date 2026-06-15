import math
k = 2 * math.sqrt(6) / 7
alpha = math.asin(k)
beta = math.pi - alpha
diff = beta - alpha
sin_half_diff = math.sin(diff / 2)
cos_alpha = math.cos(alpha)
if abs(sin_half_diff - 5/7) < 1e-9 and abs(cos_alpha - 5/7) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')