from sympy import symbols, integrate, solve, simplify, Rational

CANDIDATE = 40

# 정의
a_sym = symbols('a', positive=True, real=True)
x = symbols('x', real=True)

# 함수
def f(x_val):
    return Rational(1, 2) * x_val**3

# S1 계산
S1 = integrate(f(x), (x, 0, 1))

# b 정의
b = Rational(1, 2) * a_sym**3

# S2 계산
S2 = integrate(b - f(x), (x, 1, a_sym))
S2_simplified = simplify(S2)

# S1 = S2 방정식
eq = S1 - S2_simplified
a_solution = solve(eq, a_sym)

# a > 1인 해 찾기
valid_a = [sol for sol in a_solution if sol > 1]

if valid_a:
    a_value = valid_a[0]
    calculated_30a = 30 * a_value
    
    if abs(calculated_30a - CANDIDATE) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')