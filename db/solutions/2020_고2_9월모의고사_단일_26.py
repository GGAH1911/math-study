from sympy import *
CANDIDATE = 47

# a = 1 + log_5(9)
a = 1 + log(9, 5)
b = 2

# 원래 함수를 평행이동
x = symbols('x')
original = 5**x
translated = 5**(x - a) + b

# 주어진 목표 함수
target = Rational(1, 9) * 5**(x-1) + 2

# 몇 가지 x값에서 검증
test_values = [-1, 0, 1, 2]
success = True
for x_val in test_values:
    translated_val = float(translated.subs(x, x_val))
    target_val = float(target.subs(x, x_val))
    if abs(translated_val - target_val) > 1e-9:
        success = False
        break

# 5^a + b 계산
result = 5**a + b
result_simplified = simplify(result)

# CANDIDATE 검증
if result_simplified == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')