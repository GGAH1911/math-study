from sympy import log, simplify

a_val = 8  # 구한 답

# 좌변: log_2(8a)
lhs = log(8 * a_val) / log(2)

# 우변: 2 / log_a(2),  log_a(2) = log(2)/log(a)
log_a_2 = log(2) / log(a_val)
rhs = 2 / log_a_2

diff = simplify(lhs - rhs)

if abs(float(diff)) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
