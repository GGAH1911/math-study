from sympy import symbols, simplify, solve, Eq

x, a = symbols('x a', real=True)

# f(x) = 4/(x-3) + a
def f(expr):
    return 4/(expr - 3) + a

# f(f(x)) = x 조건
f_f_x = f(f(x))
equation = Eq(f_f_x, x)

# a = 3을 대입해서 검증
a_val = 3
equation_sub = equation.subs(a, a_val)

# 몇 가지 x 값에서 검증
test_values = [0, 1, 2, 4, 5, 10, -1]
verify = True
for x_val in test_values:
    if x_val == 3:  # 정의역 제외
        continue
    f_x = 4/(x_val - 3) + a_val
    if f_x == 3:  # f(x)=3이면 f(f(x)) 정의 불가
        continue
    f_f_x_val = 4/(f_x - 3) + a_val
    if abs(f_f_x_val - x_val) > 1e-9:
        verify = False
        break

if verify:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')