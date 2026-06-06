from sympy import sqrt, Rational, simplify, symbols, solve, Eq, Abs

# 원래 조건: AB=6, BC=8, M=BC중점, N=AC중점, AM⊥BN
# 좌표 도출: B=(0,0), C=(8,0), A=(-1, sqrt(35))

A = [Rational(-1), sqrt(35)]
B = [Rational(0), Rational(0)]
C = [Rational(8), Rational(0)]
M = [Rational(4), Rational(0)]  # BC 중점
N = [(A[0]+C[0])/2, (A[1]+C[1])/2]  # AC 중점

# 원래 조건 검증
AB_len = sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)
BC_len = sqrt((C[0]-B[0])**2 + (C[1]-B[1])**2)
assert simplify(AB_len - 6) == 0, 'AB != 6'
assert simplify(BC_len - 8) == 0, 'BC != 8'

# AM⊥BN 검증
AM_vec = (M[0]-A[0], M[1]-A[1])
BN_vec = (N[0]-B[0], N[1]-B[1])
dot = AM_vec[0]*BN_vec[0] + AM_vec[1]*BN_vec[1]
assert simplify(dot) == 0, 'AM not perp BN'

# 교점 P 구하기
t, s = symbols('t s', real=True)
Px_AM = A[0] + t*(M[0]-A[0])
Py_AM = A[1] + t*(M[1]-A[1])
Px_BN = B[0] + s*(N[0]-B[0])
Py_BN = B[1] + s*(N[1]-B[1])
sol = solve([Eq(Px_AM, Px_BN), Eq(Py_AM, Py_BN)], [t, s])
t_val = sol[t]
P = [A[0] + t_val*(M[0]-A[0]), A[1] + t_val*(M[1]-A[1])]

# ㄱ: 3AP = 2AM
AP_len = sqrt((P[0]-A[0])**2 + (P[1]-A[1])**2)
AM_len = sqrt((M[0]-A[0])**2 + (M[1]-A[1])**2)
check_gak = simplify(3*AP_len - 2*AM_len) == 0

# ㄴ: BN = sqrt(21)
BN_len = sqrt((N[0]-B[0])**2 + (N[1]-B[1])**2)
check_neun = simplify(BN_len - sqrt(21)) == 0

# ㄷ: 삼각형 ABC의 넓이 = 4*sqrt(35)
AB_v = (B[0]-A[0], B[1]-A[1])
AC_v = (C[0]-A[0], C[1]-A[1])
cross = AB_v[0]*AC_v[1] - AB_v[1]*AC_v[0]
area = Abs(cross) / 2
check_digeut = simplify(area - 4*sqrt(35)) == 0

if check_gak and check_neun and check_digeut:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: gak={check_gak}, neun={check_neun}, digeut={check_digeut}')
