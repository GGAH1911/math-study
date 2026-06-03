import sympy as sp
z = 1 + 3j
bar_z = 1 - 3j
result = z * bar_z
verify_eq = z / (2 + 1j) + bar_z / (2 - 1j)
if abs(verify_eq - 2) < 1e-10 and abs(result - 10) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')