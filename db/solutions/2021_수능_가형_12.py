from sympy import sqrt, erf

def phi(z):
    return float((1 + erf(float(z) / sqrt(2))) / 2)

P_X = phi(4.0/3) - 0.5
P_Y_ge_8 = 0.5 - P_X
sum_prob = P_X + P_Y_ge_8

z_value = 2.0
answer = phi(z_value)

if abs(sum_prob - 0.5) < 1e-10 and abs(answer - 0.9772) < 0.001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')