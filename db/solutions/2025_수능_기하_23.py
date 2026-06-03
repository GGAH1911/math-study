from sympy import symbols, Eq, solve

k = symbols('k')
vec_a = (k, 3)
vec_b = (1, 2)

# a + 3b 계산
result = (vec_a[0] + 3*vec_b[0], vec_a[1] + 3*vec_b[1])

# (6, 9)와 같아야 함
eq1 = Eq(result[0], 6)
eq2 = Eq(result[1], 9)

k_val = solve(eq1, k)[0]

# 검증
if k_val == 3:
    vec_a_actual = (3, 3)
    vec_b_actual = (1, 2)
    check = (vec_a_actual[0] + 3*vec_b_actual[0], vec_a_actual[1] + 3*vec_b_actual[1])
    if check == (6, 9):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')