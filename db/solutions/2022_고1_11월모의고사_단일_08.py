from sympy import symbols, solve, simplify

# 정의역 원소들
X = [0, 2, 4]

# a, b를 미지수로
a, b = symbols('a b', real=True)

# 각 점에서 함수값
def f(x, a_val, b_val):
    if x < 2:
        return 3*x + 2
    else:
        return x**2 + a_val*x + b_val

# 상수함수 조건: f(0) = f(2) = f(4)
f_0 = f(0, a, b)  # 3*0 + 2 = 2
f_2 = f(2, a, b)  # 4 + 2a + b
f_4 = f(4, a, b)  # 16 + 4a + b

# 조건식
eq1 = f_0 - f_2  # 2 - (4 + 2a + b) = 0
eq2 = f_2 - f_4  # (4 + 2a + b) - (16 + 4a + b) = 0

solution = solve([eq1, eq2], [a, b])
a_val = solution[a]
b_val = solution[b]

# 검증
f_0_result = 3*0 + 2
f_2_result = 2**2 + a_val*2 + b_val
f_4_result = 4**2 + a_val*4 + b_val

if f_0_result == f_2_result == f_4_result and f_0_result == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')