from sympy import symbols, Abs

x = symbols('x')
condition = Abs(x - 2) < 5

# 조건을 만족하는 정수 개수를 직접 세기
valid_integers = []
for i in range(-10, 10):
    if abs(i - 2) < 5:
        valid_integers.append(i)

count = len(valid_integers)
expected_answer = 9

if count == expected_answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')