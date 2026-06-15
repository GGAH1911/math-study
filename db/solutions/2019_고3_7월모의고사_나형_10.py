from sympy import sqrt, symbols, simplify, solve

x, a, b = symbols('x a b', real=True, positive=True)

# 원래 함수
original = sqrt(x - 1) + a

# x축으로 b, y축으로 -1 평행이동
transformed = sqrt(x - b - 1) + a - 1

# 목표 함수
target = sqrt(x - 4)

# 두 함수가 일치하는 조건
# 제곱근 내부 비교: x - b - 1 = x - 4
# 상수항 비교: a - 1 = 0

b_val = solve(-b - 1 + 4, b)[0]
a_val = solve(a - 1, a)[0]

result = a_val + b_val

# 검증
verify_func = sqrt(x - 1) + a_val
after_transform = sqrt(x - b_val - 1) + a_val - 1
after_simplify = simplify(after_transform)

if simplify(after_simplify - target) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')