import sympy as sp
x = sp.Symbol('x')

# 첫 번째 부등식: x^2 - 3x - 18 <= 0
ineq1 = x**2 - 3*x - 18 <= 0
soln1 = sp.solve(ineq1, x)

# 두 번째 부등식: x^2 - 8x + 15 >= 0
ineq2 = x**2 - 8*x + 15 >= 0
soln2 = sp.solve(ineq2, x)

# 정수해 찾기
integers = []
for i in range(-10, 20):
    if i**2 - 3*i - 18 <= 0 and i**2 - 8*i + 15 >= 0:
        integers.append(i)

sum_result = sum(integers)

if sum_result == 11:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')