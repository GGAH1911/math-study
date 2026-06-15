from sympy import log, symbols, simplify, N
a, b = symbols('a b', positive=True, real=True)
log_5_12_candidate = 2/a + b
log_2_5_val = 1/log_5_12_candidate
log_5_3_val = b
log_5_2 = 1/a
log_5_4 = 2 * log_5_2
log_5_12_true = log_5_4 + log_5_3_val
if simplify(log_5_12_candidate - log_5_12_true) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')