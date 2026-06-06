import cmath
m, n = 48, 46
z = (1 + 1j) / (2**0.5)
z_m = z**m
i_n = 1j**n
result = z_m - i_n
result_squared = result**2
if abs(result_squared - 4) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')