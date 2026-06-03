from sympy import symbols, solve, simplify
a, b = symbols('a b', real=True)
# 주어진 조건
eq1 = a + b - 2
eq2 = a**3 + b**3 - 10
# 풀이
ab = -1/3
# 검증: a + b = 2와 ab = -1/3를 만족하는 a, b 존재하는지 확인
# a^3 + b^3 = (a+b)^3 - 3ab(a+b)로 검증
result = 2**3 - 3*ab*2
if abs(result - 10) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')