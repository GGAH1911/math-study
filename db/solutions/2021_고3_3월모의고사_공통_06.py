import sympy as sp
x, a, b = sp.symbols('x a b', real=True)

# 주어진 함수의 연속 조건
# x < 3: (x^2 + ax + b)/(x-3)
# x >= 3: (2x+1)/(x-2)

# 우리 답: a=1, b=-12
a_val, b_val = 1, -12

# x < 3에서 분자
numerator_left = x**2 + a_val*x + b_val
print(f'분자 (x < 3): {numerator_left}')
print(f'x=3일 때 분자: {numerator_left.subs(x, 3)}')

# x < 3에서 극한
f_left = numerator_left / (x - 3)
left_limit = sp.limit(f_left, x, 3, '-')
print(f'좌극한: {left_limit}')

# x >= 3에서 x=3일 때
f_right = (2*x + 1) / (x - 2)
right_value = f_right.subs(x, 3)
print(f'우극한/함수값: {right_value}')

# 연속성 확인
if left_limit == right_value:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')