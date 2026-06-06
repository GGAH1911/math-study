import sympy as sp
from sympy import sqrt, symbols, solve

a_val = sqrt(10)
x = symbols('x', real=True, integer=True)

# a = sqrt(10)일 때 해 범위
ineq1 = x**2 - (a_val**2 - 3)*x - 3*a_val**2 < 0
ineq2 = x**2 + (a_val - 9)*x - 9*a_val > 0

# 수치 검증: 9 < x < 10 범위
test_x = 9.5
val1 = test_x**2 - (10 - 3)*test_x - 30
val2 = test_x**2 + (sqrt(10) - 9)*test_x - 9*sqrt(10)
print(f'At x=9.5: ineq1={val1 < 0}, ineq2={float(val2) > 0}')

# 정수 확인
for test_int in [9, 10, 11]:
    val1_int = test_int**2 - 7*test_int - 30
    val2_int = test_int**2 + (sqrt(10) - 9)*test_int - 9*sqrt(10)
    ineq1_sat = val1_int < 0
    ineq2_sat = float(val2_int) > 0
    both = ineq1_sat and ineq2_sat
    if both:
        print('VERIFY_FAIL')
        exit()

print('VERIFY_PASS')