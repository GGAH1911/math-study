from sympy import symbols, solve, simplify

# 주어진 조건
# A(-5, -1), B(a, 1)
# AB를 2:1로 외분하는 점이 y=x 위에 있음

a_sym = symbols('a', real=True)

# 외분점: 2:1로 외분하면 P = 2B - A
P_x = 2 * a_sym - (-5)
P_y = 2 * 1 - (-1)

# y = x 위의 점이므로 y좌표 = x좌표
eq = P_y - P_x

# 방정식 풀이
sol = solve(eq, a_sym)
print(f'a = {sol[0]}')

# 검증: a = -1일 때
a_val = -1
P_x_val = 2 * a_val - (-5)
P_y_val = 2 * 1 - (-1)
print(f'외분점: ({P_x_val}, {P_y_val})')
print(f'y = x 위의 점: {P_y_val == P_x_val}')

if P_y_val == P_x_val:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')