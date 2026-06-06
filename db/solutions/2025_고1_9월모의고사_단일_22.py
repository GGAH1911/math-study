import math

# 정의: nPr = n! / (n-r)!, nCr = n! / (r! * (n-r)!)
n = 4
r = 3

# 순열 계산
nPr = math.factorial(n) // math.factorial(n - r)
print(f'4P3 = {nPr}')

# 조합 계산
nCr = math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
print(f'4C3 = {nCr}')

# 합계
total = nPr + nCr
print(f'4P3 + 4C3 = {total}')

if total == 28:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')