import math
log2 = math.log(2, 10)
log10_base2 = 1 / log2
log2_20 = math.log(20, 2)
a = 2 * math.log(1/math.sqrt(10), 10) + log2_20
b = math.log(2, 10)
result = a * b
print('a =', a)
print('b =', b)
print('a * b =', result)
if abs(result - 1.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')