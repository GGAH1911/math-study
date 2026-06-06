from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 50

result = Decimal(3) / Decimal(22)
result_str = str(result)
print(f'3/22 = {result_str}')

decimals = result_str.split('.')[1]
print(f'소수 부분: {decimals[:20]}')
print(f'여섯 번째 자리: {decimals[5]}')

if decimals[5] == '3':
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')