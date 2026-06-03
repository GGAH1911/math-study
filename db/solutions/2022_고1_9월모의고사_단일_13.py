from sympy import symbols, solve

k = symbols('k')
A = (-3, 4)
B = (4, -3)
C = (6, -3 + k)

vec_AB = (B[0] - A[0], B[1] - A[1])
vec_AC = (C[0] - A[0], C[1] - A[1])

cross_product = vec_AB[0] * vec_AC[1] - vec_AB[1] * vec_AC[0]
k_value = solve(cross_product, k)[0]

if k_value == -2:
    C_check = (6, -3 + (-2))
    vec_AB_check = (7, -7)
    vec_AC_check = (C_check[0] - A[0], C_check[1] - A[1])
    cross_check = vec_AB_check[0] * vec_AC_check[1] - vec_AB_check[1] * vec_AC_check[0]
    if cross_check == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')