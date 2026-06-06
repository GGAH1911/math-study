import cmath

z = 1 - 1j
z_conj = 1 + 1j

valid_n = []
for n in range(1, 11):
    term1 = (z_conj / z) ** (2*n)
    term2 = (z / cmath.sqrt(2)) ** (2*n)
    result = term1 + term2
    if abs(result) < 1e-10:
        valid_n.append(n)

if valid_n == [2, 6, 10] and sum(valid_n) == 18:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')