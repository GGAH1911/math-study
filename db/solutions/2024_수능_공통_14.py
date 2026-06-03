from sympy import *
x = symbols('x', real=True)

# k = -3에서 조건 확인 (a=48, b=3)
a, b = 48, 3

# x <= 2: f(x) = -3의 해
f1 = 2*x**3 - 6*x + 1 + 3
roots_f1 = solve(f1, x)
print(f'x<=2에서 f(x)=-3의 실근: {roots_f1}')

# x > 2: 극소값 = -3인지 확인
min_val = 9 - a * (b-2)**2/4
print(f'x>2의 극소값: {min_val}')

if min_val == -3 and all(r.is_real for r in roots_f1):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')