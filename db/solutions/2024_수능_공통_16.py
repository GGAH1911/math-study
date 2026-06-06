from sympy import symbols, Eq, solve, simplify

x = symbols('x')

# 원래 방정식: 3^(x-8) = (1/27)^x
# 좌변: 3^(x-8)
# 우변: (1/27)^x = (3^(-3))^x = 3^(-3x)

eq = Eq(3**(x-8), 3**(-3*x))
solutions = solve(eq, x)

if solutions:
    x_val = solutions[0]
    # 역대입 검증
    lhs = 3**(x_val - 8)
    rhs = (1/27)**x_val
    
    # 수치 비교
    lhs_float = float(lhs)
    rhs_float = float(rhs)
    
    if abs(lhs_float - rhs_float) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')