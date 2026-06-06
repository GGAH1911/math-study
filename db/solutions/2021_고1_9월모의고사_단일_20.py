import cmath
z = (-1 + cmath.sqrt(3)*1j) / 2

# Check ㄱ: z^3 = 1
result_ga = z**3
assert abs(result_ga - 1) < 1e-10, f'ㄱ failed: z^3 = {result_ga}'

# Check ㄴ: z^4 + z^5 = -1
result_na = z**4 + z**5
assert abs(result_na - (-1)) < 1e-10, f'ㄴ failed: z^4+z^5 = {result_na}'

# Check ㄷ: Count n where z^n + z^{2n} + z^{3n} + z^{4n} + z^{5n} = -1
count = 0
for n in range(1, 101):
    s = z**n + z**(2*n) + z**(3*n) + z**(4*n) + z**(5*n)
    if abs(s - (-1)) < 1e-10:
        count += 1

assert count == 67, f'ㄷ count is {count}, not 66'
print('VERIFY_PASS')