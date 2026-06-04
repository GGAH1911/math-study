# f가 연속이므로 lim(x→1) f(x) = f(1)
# 주어진 조건: lim(x→1)(f(x)+5) = 2*f(1)
# f(1)을 구하려는 것

f_1 = 5  # 우리의 답

# 검증: f(1) + 5 = 2*f(1) 만족하는가?
lhs = f_1 + 5  # 좌변
rhs = 2 * f_1  # 우변

if lhs == rhs:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')