from math import comb

a = 2

# (2+x)^5 전개
coeff_x5 = [comb(5, k) * (2**(5-k)) for k in range(6)]
print('(2+x)^5 계수:', coeff_x5)

# (1+ax)(2+x)^5에서 x^3과 x^4 계수
coeff_x3 = coeff_x5[3] + a * coeff_x5[2]
coeff_x4 = coeff_x5[4] + a * coeff_x5[3]

print(f'x^3 계수: {coeff_x3}')
print(f'x^4 계수: {coeff_x4}')
print(f'합: {coeff_x3 + coeff_x4}')

if coeff_x3 + coeff_x4 == 290:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')