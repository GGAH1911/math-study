from sympy import symbols, expand

# 원래 문제의 다항식
def P(x):
    return x**4 + x**3 + 2*x - 4

def Q_func(x, a, b):
    return x**4 + x**3 + a*x**2 + b*x + 1

# 찾은 답: b = -1, a = -2
b_val = -1
a_val = -2

# 조건 검증: P(-b) = 0
P_check = P(-b_val)
if P_check != 0:
    print('VERIFY_FAIL')
else:
    # 조건 검증: Q(-b) = 0
    Q_check = Q_func(-b_val, a_val, b_val)
    if Q_check != 0:
        print('VERIFY_FAIL')
    else:
        # 최종 답 검증
        result = P(b_val) + Q_func(a_val, a_val, b_val)
        if result == -3:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')