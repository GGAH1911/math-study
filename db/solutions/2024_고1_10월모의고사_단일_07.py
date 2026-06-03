# 검증: $R(x) = 2x + 4$
a, b = 2, 4
R_1 = a * 1 + b
print(f'R(1) = {R_1}')

# 원래 조건 확인
R_minus2 = a * (-2) + b
R_4 = a * 4 + b
print(f'R(-2) = {R_minus2} (P(-2)과 같아야 함, 0이어야 함)')
print(f'R(4) = {R_4} (P(4)의 나머지와 같아야 함, 12이어야 함)')

if R_minus2 == 0 and R_4 == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')