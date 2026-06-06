from sympy import *
import numpy as np

a = symbols('a', real=True)

# 3^a + 3^(-a) = 4를 만족하는 a 찾기
eq1 = 3**a + 3**(-a) - 4
sol_a = solve(eq1, a)

if sol_a:
    a_val = sol_a[0]
    
    # 검증 1: 원래 등식 (3^a + 3^(-a))^2 = 2(3^a + 3^(-a)) + 8
    lhs = (3**a_val + 3**(-a_val))**2
    rhs = 2*(3**a_val + 3**(-a_val)) + 8
    
    lhs_simplified = simplify(lhs)
    rhs_simplified = simplify(rhs)
    
    check1 = simplify(lhs_simplified - rhs_simplified) == 0
    
    # 검증 2: 27^a + 27^(-a) 계산
    result = 27**a_val + 27**(-a_val)
    result_simplified = simplify(result)
    
    # 수치 검증
    t_val = 3**float(a_val) + 3**(-float(a_val))
    result_numeric = 27**float(a_val) + 27**(-float(a_val))
    
    if check1 and abs(result_simplified - 52) < 1e-6:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    # 직접 계산: 3^a + 3^(-a) = 4일 때
    # 3^(3a) + 3^(-3a) = (3^a + 3^(-a))^3 - 3(3^a + 3^(-a))
    t = 4
    result = t**3 - 3*t
    if result == 52:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')