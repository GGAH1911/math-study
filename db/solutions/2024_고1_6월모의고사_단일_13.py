from sympy import symbols, solve, simplify, discriminant

x, y, k = symbols('x y k', real=True)

# 원래 연립방정식
eq1 = x - y - 3
eq2 = x**2 - x*y - y**2 - k

# y = x - 3을 두 번째 식에 대입
eq2_sub = eq2.subs(y, x - 3)
eq2_sub = simplify(eq2_sub)

# x에 대한 이차방정식 계수
# x^2 - 9x + (9+k) = 0
quadratic_eq = x**2 - 9*x + (9 + k)

# k = 11일 때 판별식 확인
k_val = 11
disc = 81 - 4*(9 + k_val)

if disc > 0:
    alpha, beta = solve(x**2 - 9*x + 20, x)
    alpha, beta = float(alpha), float(beta)
    
    # 원래 방정식 검증
    result1 = alpha**2 - alpha*(alpha-3) - (alpha-3)**2
    result2 = beta**2 - beta*(beta-3) - (beta-3)**2
    
    if abs(result1 - k_val) < 1e-9 and abs(result2 - k_val) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')