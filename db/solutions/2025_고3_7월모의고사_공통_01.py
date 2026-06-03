import math
import sympy as sp

# 원래 문제: √3 × √3 의 값
result_numeric = math.sqrt(3) * math.sqrt(3)
result_symbolic = sp.simplify(sp.sqrt(3) * sp.sqrt(3))

print(f'수치 계산: {result_numeric}')
print(f'기호 계산: {result_symbolic}')

if abs(result_numeric - 3.0) < 1e-10 and result_symbolic == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')