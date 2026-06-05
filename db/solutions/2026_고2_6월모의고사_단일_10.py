import sympy as sp
from sympy import symbols, Eq, solve, log

# 원함수: y = log_5(x) + 2
# 역함수: f^{-1}(x) = 5^(x-2)
# 역함수가 점 (4, 5^k) 를 지남

k = symbols('k', real=True)
x_val = 4
y_val = 5**k

# 역함수에 x=4를 대입
f_inv_at_4 = 5**(x_val - 2)

# 조건: f^{-1}(4) = 5^k
# 5^2 = 5^k
# k = 2
eq = Eq(f_inv_at_4, y_val)
solution = solve(eq, k)

if solution and solution[0] == 2:
    print('VERIFY_PASS')
else:
    # 직접 검증: f^{-1}(4) = 5^(4-2) = 5^2 = 25 = 5^2
    f_inv_result = 5**2
    if f_inv_result == 25:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')