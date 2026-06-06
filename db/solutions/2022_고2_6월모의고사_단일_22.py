import sympy as sp
result = 4**(3/2) * 2**2
expected_answer = 32
if abs(result - expected_answer) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')