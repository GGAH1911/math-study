import sympy as sp
from sympy import log, simplify, N

# 원래 식 계산: log_3(25) * (log_5(9) + log_25(3))
log3_25 = log(25, 3)
log5_9 = log(9, 5)
log25_3 = log(3, 25)

result = log3_25 * (log5_9 + log25_3)
result_simplified = simplify(result)
result_value = N(result_simplified)

print(f'log_3(25) * (log_5(9) + log_25(3)) = {result_simplified} = {result_value}')

if abs(result_value - 5) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')