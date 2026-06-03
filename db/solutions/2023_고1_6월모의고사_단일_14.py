from sympy import symbols, Eq, solve, Rational

# 변수 정의
n1, n2, P1, P2, R, T = symbols('n1 n2 P1 P2 R T', positive=True, real=True)

# 이상기체 법칙: PV = nRT
# V1 = n1*R*T / P1
# V2 = n2*R*T / P2

# 주어진 조건
# n1 = (1/4) * n2
# P1 = (3/2) * P2

# n2 = 4*n1, P2 = (2/3)*P1로 정리
V1 = n1 * R * T / P1
V2 = (4*n1) * R * T / ((Rational(2,3)*P1))

ratio = V1 / V2
ratio_simplified = ratio.simplify()

if ratio_simplified == Rational(1, 6):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')