from sympy import symbols, solve, Rational
a = symbols('a')
# 조건: -5 < (2a+1)/3 <= 3
# 좌측: -5 < (2a+1)/3
left_ineq = -5 < Rational(1,3)*(2*a + 1)
left_sol = solve(left_ineq, a)
# 우측: (2a+1)/3 <= 3  
right_ineq = Rational(1,3)*(2*a + 1) <= 3
right_sol = solve(right_ineq, a)
# a > -8 and a <= 4
integers = [i for i in range(-10, 10) if -8 < i <= 4]
min_a = min(integers)
max_a = max(integers)
result = min_a + max_a
if result == -3:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result} instead of -3')