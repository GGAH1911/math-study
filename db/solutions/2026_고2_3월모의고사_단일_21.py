from sympy import Rational, sqrt

# Geometric verification
k = Rational(3, 2)
A = (12, 18)
B = (8, 12)

# A, B on circle (x-13)^2 + (y-13)^2 = 26
assert (A[0]-13)**2 + (A[1]-13)**2 == 26, 'A not on circle'
assert (B[0]-13)**2 + (B[1]-13)**2 == 26, 'B not on circle'

# A, B on line y = kx
assert A[1] == k * A[0], 'A not on y=kx'
assert B[1] == k * B[0], 'B not on y=kx'

# |AB| = 2*sqrt(13)
AB_len = sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)
assert AB_len == 2*sqrt(13), f'|AB|={AB_len}'

# distance from (13,13) to y=kx equals sqrt(13)
d = 13*(k-1)/sqrt(k**2+1)
assert d == sqrt(13), f'd={d}'

# f(8)=12, f(12)=18 => f_inv(12)=8, f_inv(18)=12
# g(x) = f_inv(x) - 2
# Solve g(x) = (1/k)*x - 2 = (2/3)*x - 2
# => f_inv(x) = (2/3)*x
# => f(y) = (3/2)*y, solutions y=8 (x=12) and y=12 (x=18)

# Verify x=12: g(12) = f_inv(12) - 2 = 8 - 2 = 6; rhs = (2/3)*12 - 2 = 6
alpha = 12
g_alpha = 8 - 2  # f_inv(12) = 8
rhs_alpha = Rational(1,1)/k * alpha - 2
assert g_alpha == rhs_alpha, f'g(12)={g_alpha}, rhs={rhs_alpha}'

# Verify x=18: g(18) = f_inv(18) - 2 = 12 - 2 = 10; rhs = (2/3)*18 - 2 = 10
beta = 18
g_beta = 12 - 2  # f_inv(18) = 12
rhs_beta = Rational(1,1)/k * beta - 2
assert g_beta == rhs_beta, f'g(18)={g_beta}, rhs={rhs_beta}'

assert beta - alpha == 6
print('VERIFY_PASS')
