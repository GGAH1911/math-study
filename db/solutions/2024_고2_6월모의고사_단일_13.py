from fractions import Fraction
count = 0
valid = []
for x in range(-10, 10):
    lhs = Fraction(2**(2*x+3) + 2)
    rhs = Fraction(17 * 2**x)
    if lhs <= rhs:
        count += 1
        valid.append(x)
expected = 5
print(f'만족하는 정수 x: {valid}')
print(f'개수: {count}')
if count == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')