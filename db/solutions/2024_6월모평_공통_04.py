# 검증: f(1) = 2일 때 조건 만족 확인
f_1 = 2

# 조건: lim f(x) = 4 - f(1)
# 연속성: lim f(x) = f(1)
# 따라서: f(1) = 4 - f(1)

lhs = f_1  # f(1)
rhs = 4 - f_1  # 4 - f(1)

if lhs == rhs:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')