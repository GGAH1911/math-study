import sympy as sp
from sympy import log, symbols, solve

x = symbols('x')  # log_3(5)

# 주어진 원래 조건식
# 3a + b = log_3(45) = log_3(3^2 * 5) = 2 + x
# a + b = log_9(5) = log_3(5)/2 = x/2

# a, b를 변수로 정의
a, b = symbols('a b', real=True)
eq1 = 3*a + b - (2 + x)
eq2 = a + b - x/2

# 연립방정식 풀기
sol = solve([eq1, eq2], [a, b])
a_val = sol[a]
b_val = sol[b]

# a - b 계산
diff = a_val - b_val
diff_simplified = sp.simplify(diff)

# x = log_3(5)를 대입해도 diff = 2인지 확인
if diff_simplified == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')