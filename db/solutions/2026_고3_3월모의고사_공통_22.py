import math
from sympy import *

k = 2
u = symbols('u', positive=True, real=True)
h = 2*u**2 - u + Rational(1,4)

# h(u) = 1/5의 해
eq1 = Eq(h, Rational(1,5))
sols1 = solve(eq1, u)
print(f'h(u) = 1/5의 해: {len(sols1)}개, 모두 양수: {all(sol > 0 for sol in sols1)}')

# h(u) = -1/5의 해
eq2 = Eq(h, Rational(-1,5))
sols2 = solve(eq2, u)
print(f'h(u) = -1/5의 해: {len(sols2)}개')

total_solutions = len([s for s in sols1 if s > 0]) + len([s for s in sols2 if s > 0])
print(f'총 양의 해: {total_solutions}개')

# u_1 * u_2 = 1/40 확인
if len(sols1) == 2:
    product = sols1[0] * sols1[1]
    print(f'u_1 * u_2 = {simplify(product)}')
    p = log(product, 2)
    result = 2 * (Rational(1,2))**p
    result_simplified = simplify(result)
    print(f'k * (1/2)^p = {result_simplified}')
    if result_simplified == 80:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')