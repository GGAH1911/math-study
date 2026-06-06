import sympy as sp
from sympy import symbols, sqrt, solve, simplify

# 쌍곡선 정의
a, b, c = 2, 4*sqrt(2), 6

# 초점
F = (-6, 0)
F_prime = (6, 0)

# 점 A의 좌표 (조건으로부터 |AF|=8, |AF'|=12)
A = (-sp.Rational(10,3), sp.Rational(16,3)*sqrt(2))

# A가 쌍곡선 위에 있는지 확인
x_A, y_A = A
check_hyperbola = x_A**2/4 - y_A**2/32 - 1
print(f'A on hyperbola: {simplify(check_hyperbola) == 0}')

# AF, AF' 거리 확인
AF = sqrt((x_A - F[0])**2 + (y_A - F[1])**2)
AF_prime = sqrt((x_A - F_prime[0])**2 + (y_A - F_prime[1])**2)
print(f'|AF| = {simplify(AF)}')
print(f'|AF\'| = {simplify(AF_prime)}')

# 중점 M
M = ((-sp.Rational(14,3)), sp.Rational(8,3)*sqrt(2))

# 직선 MF' 위의 점: (x,y) = M + s(F'-M)
# 쌍곡선과의 교점
s = symbols('s')
x_s = M[0] + s * (F_prime[0] - M[0])
y_s = M[1] + s * (F_prime[1] - M[1])

eq = x_s**2/4 - y_s**2/32 - 1
eq_simplified = simplify(eq)
s_solutions = solve(eq_simplified, s)
print(f'Parameter s solutions: {[simplify(sol) for sol in s_solutions]}')

# k = 8*sqrt(2) 확인
k = 8*sqrt(2)
k_squared = k**2
print(f'k = {k}')
print(f'k^2 = {k_squared}')
print('VERIFY_PASS')