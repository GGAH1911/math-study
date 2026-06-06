import math

p = 1/3
f_pi6 = math.sin(3 * math.pi / 6)  # sin(π/2)
g_pi12 = math.sin(2 * math.pi / 12)  # sin(π/6)

result = p * f_pi6 * g_pi12
expected = 1/6

if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')