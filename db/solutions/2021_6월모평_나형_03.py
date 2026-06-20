from sympy import symbols, Eq, solve

# 등차수열 조건: a1 + a3 = 20
# a1 = a, a3 = a + 2d이므로
# a + (a + 2d) = 20
# 2a + 2d = 20
# a + d = 10
# a2 = a + d = 10

a, d = symbols('a d', real=True)
eq = Eq(a + (a + 2*d), 20)

# a + d를 구하면 a2
# 2a + 2d = 20에서 a + d = 10
a2_value = 10

# 검증: a1 + a3 = 20을 만족하는지 확인
# a + d = 10이면, a = 10 - d
# a1 + a3 = (10-d) + (10-d+2d) = (10-d) + (10+d) = 20
verify = (10 - d) + (10 - d + 2*d)
verify_simplified = verify.simplify()

if verify_simplified == 20:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')