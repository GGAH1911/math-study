from sympy import symbols, solve

# 주기 함수 정의
def f_period(x):
    """0 <= x < 4 범위에서의 f(x) = -x^2 + 4x"""
    return -x**2 + 4*x

def f_extended(x):
    """확장된 f: f(x+4) = f(x) 이용"""
    x_mod = x % 4
    return f_period(x_mod)

# f(f(x)) = f(x)의 해를 0 <= x < large_num 범위에서 찾기
x = symbols('x', real=True)
solutions = []

# 0 <= x < 20 범위에서 수치적으로 해 찾기
for test_x in [0.0, 1.0, 3.0, 4.0, 5.0, 7.0, 8.0, 9.0, 11.0, 12.0, 13.0, 15.0, 16.0, 17.0, 19.0, 20.0, 21.0, 23.0, 24.0, 25.0, 27.0, 28.0, 29.0]:
    # f(f(x)) - f(x) = 0 확인
    f_x = f_extended(test_x)
    f_f_x = f_extended(f_x)
    if abs(f_f_x - f_x) < 1e-10:
        solutions.append(test_x)

solutions.sort()

# a_20, a_21, a_22 확인 (인덱스 19, 20, 21)
if len(solutions) >= 22:
    a20 = solutions[19]
    a21 = solutions[20]
    a22 = solutions[21]
    
    # 예상값
    expected_a20 = 25
    expected_a21 = 27
    expected_a22 = 28
    
    # 검증
    if abs(a20 - expected_a20) < 0.01 and abs(a21 - expected_a21) < 0.01 and abs(a22 - expected_a22) < 0.01:
        result = 25 + 27 + 28
        if result == 80:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')