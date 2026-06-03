import sympy as sp
n, x = sp.symbols('n x')
# 원 문제: 곡선 y=x^2-2nx-2n, 직선 y=x+1의 교점 P_n, Q_n
roots = sp.solve(x**2 - 2*n*x - 2*n - (x + 1), x)
alpha, beta = roots
# 점 P=(alpha, alpha+1), Q=(beta, beta+1) 사이 거리 제곱
d2 = sp.simplify((alpha - beta)**2 + ((alpha + 1) - (beta + 1))**2)
# 대각선 길이가 d 인 정사각형 넓이 = d^2/2
a_n = sp.simplify(d2 / 2)
# 부분합 N 까지 수치로도 비교, 그리고 무한합 기호적으로 계산
S_inf = sp.simplify(sp.summation(1 / a_n, (n, 1, sp.oo)))
expected = sp.Rational(2, 15)
# 추가 수치 검증: N=2000 부분합과 비교
S_partial = sum(1 / ((2*k + 1) * (2*k + 5)) for k in range(1, 2001))
num_ok = abs(float(S_partial) - float(expected)) < 1e-3
if sp.simplify(S_inf - expected) == 0 and num_ok:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
