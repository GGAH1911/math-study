import math
m = -12
# Calculate f(m) = f(-12)
value = abs(5 * math.log2(4 - (-12)) + m)
print(f'f(-12) = |5*log2(16) + (-12)| = |5*4 - 12| = {value}')
if value == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')