from sympy import symbols, limit, Rational

CANDIDATE = '16'

x = symbols('x', real=True)

# 주어진 조건을 만족하는 함수 구성
# 조건 1: lim_{x→1} f(x)/(x-1) = 8
# 조건 2: lim_{x→1} g(x)/(x^2-1) = 1/2

# 가장 간단한 함수: f(x) = 8(x-1)
f = 8 * (x - 1)

# 조건 2를 만족하는 함수: g(x) = (1/2)(x^2-1)
g = Rational(1, 2) * (x**2 - 1)

# 조건 1 검증: lim_{x→1} f(x)/(x-1) = 8
limit1 = limit(f / (x - 1), x, 1)

# 조건 2 검증: lim_{x→1} g(x)/(x^2-1) = 1/2
limit2 = limit(g / (x**2 - 1), x, 1)

# 구하는 극한값 계산: lim_{x→1} (x+1)f(x)/g(x)
result = limit((x + 1) * f / g, x, 1)

# CANDIDATE와 비교하여 검증
if limit1 == 8 and limit2 == Rational(1, 2) and result == int(CANDIDATE):
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")