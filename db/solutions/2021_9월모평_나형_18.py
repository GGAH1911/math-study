from sympy import *
a = 2
x = symbols('x', real=True)
f_prime = 2*a*(x - 1)
condition = 4*x**2 + 5
# 임계점 검증
for x_val in [-0.5, 2.5]:
    lhs = abs(f_prime.subs(x, x_val))
    rhs = condition.subs(x, x_val)
    if abs(float(lhs - rhs)) < 1e-9:
        print(f'Equality at x={x_val}: {float(lhs)}={float(rhs)}')
# 일반 부등식 검증: 최솟값이 0 이상인지 확인
ineq_pos = condition - f_prime
ineq_neg = condition + f_prime
roots_pos = solve(4*x**2 - 8*x - 5, x)
min_val = min(float(ineq_pos.subs(x, float(r))) for r in roots_pos if float(r) > 1)
min_val2 = min(float(ineq_neg.subs(x, float(r))) for r in roots_pos if float(r) < 1)
if min_val >= -1e-9 and min_val2 >= -1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')