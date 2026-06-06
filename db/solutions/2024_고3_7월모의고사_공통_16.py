import sympy as sp
x = sp.Symbol('x', real=True)

# 원래 방정식의 정의역 조건
cond1 = x + 9 > 0
cond2 = x - 6 > 0

# x = 11 대입
x_val = 11

# 정의역 확인
if x_val + 9 > 0 and x_val - 6 > 0:
    # 좌변: log_5(x+9)
    left = sp.log(x_val + 9, 5)
    # 우변: log_5(4) + log_5(x-6)
    right = sp.log(4, 5) + sp.log(x_val - 6, 5)
    
    # 우변을 정리하면: log_5(4 * 5) = log_5(20)
    right_simplified = sp.log(4 * (x_val - 6), 5)
    
    if sp.simplify(left - right) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')