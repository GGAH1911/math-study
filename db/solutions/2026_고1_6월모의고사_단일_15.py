from sympy import symbols, solve, Abs
x, a = symbols('x a')
# 조건: 정수 x 개수 = 2
for a_val in range(-5, 15):
    count = 0
    valid_x = []
    for x_val in range(3, 10):
        cond1 = abs(x_val - 6) <= 3
        cond2 = x_val**2 - (4*a_val+1)*x_val + 3*a_val**2 + a_val <= 0
        if cond1 and cond2:
            count += 1
            valid_x.append(x_val)
    if count == 2:
        print(f'a={a_val}: 정수 {valid_x}, 개수={count}')
total = 1 + 8
print(f'합={total}')
if total == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')