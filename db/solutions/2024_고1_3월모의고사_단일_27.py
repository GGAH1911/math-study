from fractions import Fraction

values = [Fraction(-1, 2), Fraction(6, 5), Fraction(-3, 4), Fraction(2, 9)]

products = []
for i in range(len(values)):
    for j in range(i+1, len(values)):
        products.append(values[i] * values[j])

a = max(products)
b = min(products)

result = 120 * (a - b)

if result == 153:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')