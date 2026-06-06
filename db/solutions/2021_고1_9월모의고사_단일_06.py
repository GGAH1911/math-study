# 첫 번째 부등식: x + 3 < 3x
# x > 3/2

# 두 번째 부등식: 3x + 4 < 2x + 8
# x < 4

a = 3/2
b = 4
ab = a * b

# 경계값 검증
# x = 3/2 근처 (약간 크게)
x_test1 = 1.6
ineq1_pass = (x_test1 + 3 < 3*x_test1)
ineq2_pass = (3*x_test1 + 4 < 2*x_test1 + 8)

# x = 4 근처 (약간 작게)
x_test2 = 3.9
ineq1_pass2 = (x_test2 + 3 < 3*x_test2)
ineq2_pass2 = (3*x_test2 + 4 < 2*x_test2 + 8)

if (ab == 6 and ineq1_pass and ineq2_pass and ineq1_pass2 and ineq2_pass2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')