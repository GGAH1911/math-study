from sympy import *

# 매개변수 a = 2
a = 2

# f(x) = (x-2)^2(x+1) - 2
def f(x_val):
    return (x_val - 2)**2 * (x_val + 1) - 2

# g(x) 정의
def g(x_val):
    if 0 < x_val < 2:
        return a - abs(f(x_val))
    else:
        return abs(f(x_val)) - a

# g(3a) = g(6) 계산
result = g(6)
print(f'f(6) = {f(6)}')
print(f'|f(6)| = {abs(f(6))}')
print(f'g(6) = {result}')

# 검증: 조건 (가) 확인
x_test = 3.0
lhs = abs(x_test * (x_test - 2)) * g(x_test)
rhs = x_test * (x_test - 2) * (abs(f(x_test)) - a)
print(f'\n조건 (가) 검증 (x=3): LHS={lhs:.6f}, RHS={rhs:.6f}, 일치={abs(lhs-rhs)<1e-10}')

if result == 108:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')