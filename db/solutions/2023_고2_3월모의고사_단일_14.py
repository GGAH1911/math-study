import sympy as sp
x, a = sp.symbols('x a', real=True)

# a = -1 대입
a_val = -1

# 부등식 1: x^2 + 3x - 10 < 0
ineq1_roots = sp.solve(x**2 + 3*x - 10, x)
print(f'부등식 1 근: {ineq1_roots}')
# 범위: -5 < x < 2

# 부등식 2: a*x >= a^2 with a = -1
# -1*x >= 1 => x <= -1
ineq2_bound = a_val  # x <= -1

# 정수 개수 확인
integer_count = 0
valid_integers = []
for int_x in range(-10, 10):
    cond1 = (int_x**2 + 3*int_x - 10) < 0
    cond2 = (a_val * int_x) >= (a_val**2)
    if cond1 and cond2:
        integer_count += 1
        valid_integers.append(int_x)

print(f'정수 해: {valid_integers}')
print(f'개수: {integer_count}')

if integer_count == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')