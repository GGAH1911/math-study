from sympy import symbols, sqrt, simplify

# 주어진 점들
a, b, c = 1, 6, 12
O = (0, 0)
A = (a, 7)
B = (b, c)
C = (5, 5)

# 마름모 조건 1: 모든 변의 길이가 같음
OA_len_sq = (A[0] - O[0])**2 + (A[1] - O[1])**2
AB_len_sq = (B[0] - A[0])**2 + (B[1] - A[1])**2
BC_len_sq = (C[0] - B[0])**2 + (C[1] - B[1])**2
CO_len_sq = (O[0] - C[0])**2 + (O[1] - C[1])**2

cond1 = OA_len_sq == AB_len_sq == BC_len_sq == CO_len_sq

# 마름모 조건 2: 대각선이 서로를 이등분
OB_midpoint = ((O[0] + B[0])/2, (O[1] + B[1])/2)
AC_midpoint = ((A[0] + C[0])/2, (A[1] + C[1])/2)

cond2 = OB_midpoint == AC_midpoint

# 마름모 조건 3: 대각선이 수직
OB_vec = (B[0] - O[0], B[1] - O[1])
AC_vec = (C[0] - A[0], C[1] - A[1])
dot_product = OB_vec[0] * AC_vec[0] + OB_vec[1] * AC_vec[1]

cond3 = dot_product == 0

if cond1 and cond2 and cond3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')